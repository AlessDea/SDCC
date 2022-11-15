from concurrent import futures
import logging
import grpc
import mysql.connector
import pika
from pika.exchange_type import ExchangeType
import json
import threading

from protos.login_pb2 import *
from protos.login_pb2_grpc import *
from protos.groupmanager_pb2_grpc import *
from protos.groupmanager_pb2 import *
from lib.breaker_listeners import *

breaker = pybreaker.CircuitBreaker(fail_max=2, reset_timeout=5, listeners=[GreetingsListener(), LogListener()])

connection = None
channel = None


def connect_rabbitmq():
    try:
        connection_parameters = pika.ConnectionParameters('rabbitmq.default.svc.cluster.local')
        pika_connection = pika.BlockingConnection(connection_parameters)
        return pika_connection
    except:
        return False


def connect_mysql_primary():
    try:
        connection = mysql.connector.connect(
            host="group-db-mysql-primary.default.svc.cluster.local",
            user="root",
            password="root",
            database="mydb",
            port="3306"
        )
        return connection
    except:
        return False


def connect_mysql_secondary():
    try:
        connection = mysql.connector.connect(
            host="group-db-mysql-secondary.default.svc.cluster.local",
            user="root",
            password="root",
            database="mydb",
            port="3306"
        )
        return connection
    except:
        return connect_mysql_primary()


def get_emails(group_name, service):

    query = "SELECT email FROM team WHERE group_name = %s AND service = %s"
    val = (group_name, service)

    mydb = connect_mysql_secondary()
    mycursor = None
    emails = []

    if mydb != False:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(query, val)
            myresult = mycursor.fetchall()
            if mycursor.rowcount > 0:
                for res in myresult:
                    emails.append(res[0])
                return emails
            return None
        except:
            return None
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return None


def groupCreate(group_name, emails, agency):

    mydb = connect_mysql_primary()
    mycursor = None

    val = []

    for email in emails:
        val.append(tuple([group_name, email, agency]))

    if mydb != False:
        try:
            query = "INSERT INTO team VALUES (%s,%s,%s)"
            mycursor = mydb.cursor()
            mycursor.executemany(query,val)
            mydb.commit()
            if mycursor.rowcount > 0:
                return 0
            return -1
        except:
            return -1
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return -1


def groupList(email):
    group_names  = []
    services     = []
    dictionary   = {}

    query = "SELECT group_name, service FROM team WHERE email = %s"

    mydb = connect_mysql_secondary()
    mycursor = None

    if mydb != False:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(query,(email,))
            myresult = mycursor.fetchall()
            for i in range (0, mycursor.rowcount):
                group_names.append(myresult[i][0])
                services.append(myresult[i][1])
            dictionary = dict(zip(group_names, services))
            return dictionary
        except:
            return dictionary
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return dictionary

@breaker
def checkUserAgency(emails, agency):

    for email in emails:
        try:
            with grpc.insecure_channel('login-service:50052') as channel:
                stub = LoginStub(channel)
                response = stub.checkEmployee(CheckEmployeeRequest(email=email, agency=agency))

                if response.isEmployeeChecked != 0:
                    return response.isEmployeeChecked       # può ritornare -1, 1, 2
        except:
            raise Exception
    return response.isEmployeeChecked                       # ritorna 0


# Publish on RabbitMQ the request for Shared Password. Queue info_queue
def publishEmailsList(group_name, email_applicant, email_list, service):

    connection = connect_rabbitmq()
    if connection != False:
        try:
            message = {'group_name':group_name, 'email_applicant':email_applicant, 'participants':email_list, 'service':service}
            body = json.dumps(message)

            channel = connection.channel()
            channel.exchange_declare(exchange='routing', exchange_type=ExchangeType.direct, durable=True)
            channel.basic_publish(exchange='routing', routing_key='sharedpassword', body=body, properties=pika.BasicProperties(delivery_mode=2,))
            connection.close()
            logging.warning('Rabbitmq group manager publish')
            return True
        except:
            logging.warning('Rabbitmq Exception publish')
            return False
    else:
        logging.warning('Rabbitmq publish else')
        return False


# Consume from RabbitMQ the request from Shared Password. Queue request_queue
def on_message_received(channel, method, properties, body):

    dictionary = json.loads(body)

    group_name = dictionary['group_name']
    email_applicant = dictionary['email']
    service = dictionary['service']

    email_list = get_emails(group_name,service)

    logging.warning('on_message_received - Group: ' + str(group_name) + " Email_applicant: " + str(email_applicant) + " Service: " + str(service) + " list: " + str(email_list))

    # This branch it should never be taken, the Shared Password
    # can only be requested from the Group List page
    if email_list == None:
        return False

    # Remove from the email_list the applicant one
    email_list.remove(str(email_applicant))
    logging.warning('Lista remove: ' + str(email_list))

    # Publish on RabbitMQ the group infos required to send emails
    response = publishEmailsList(group_name, email_applicant, email_list, service)
    
    # Send ack only if there were no errors
    # (try/except not required, at worst multiple requests are sent and only the last one is valid)
    if response:
        channel.basic_ack(delivery_tag=method.delivery_tag, multiple=False)
        logging.warning('Rabbitmq groupmanager ack sent' + str(response))
        return True
    return False


class GroupManager(GroupManagerServicer):

    def groupCreate(self, request, context):

        check = checkUserAgency(request.emails, request.agency)

        try:
            if check == 0:
                response = groupCreate(request.group_name, request.emails, request.agency)
                return GroupCreateReply(isCreated=response)
            return GroupCreateReply(isCreated=check)
        except:
            raise Exception

    def groupList(self, request, context):
        response = groupList(request.email)
        return GroupListReply(list=response)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_GroupManagerServicer_to_server(GroupManager(), server)
    server.add_insecure_port('[::]:50057')
    server.start()
    server.wait_for_termination()


def consumingRequestQueue():
    connection = connect_rabbitmq()
    logging.warning('Rabbitmq connection: ' + str(connection))
    if connection != False:
        try:
            channel = connection.channel()
            logging.warning('Rabbitmq connection 1')
            channel.exchange_declare(exchange='routing', exchange_type=ExchangeType.direct, durable=True)
            logging.warning('Rabbitmq connection: 2')
            channel.queue_declare(queue='request_queue', durable=True)
            logging.warning('Rabbitmq connection: 3')
            channel.queue_bind(exchange='routing', queue='request_queue', routing_key='groupmanager')
            logging.warning('Rabbitmq connection: 4')
            channel.basic_qos(prefetch_count=1)   # Remove this line to let RabbitMQ act in round robin manner
            logging.warning('Rabbitmq connection: 5')
            channel.basic_consume(queue='request_queue', on_message_callback=on_message_received)
            logging.warning('Rabbitmq connection: 6')
            channel.start_consuming()
        except Exception as e:
            logging.warning('Rabbitmq Exception: ' + str(e))
            return False
    else:
        return False


if __name__ == '__main__':

    logging.basicConfig()

    grpcThread = threading.Thread(target=serve)
    grpcThread.start()

    while True:
        rabbitmqThread = threading.Thread(target=consumingRequestQueue)
        logging.warning('\n\n\nAvvio thread rabbitmq')
        rabbitmqThread.start()
        rabbitmqThread.join()
        logging.warning('Join thread rabbitmq')

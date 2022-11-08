from concurrent import futures
import logging
import grpc
import mysql.connector
import pika
from pika.exchange_type import ExchangeType
import json

from protos.sharedpw_pb2 import *
from protos.sharedpw_pb2_grpc import *
from protos.newpassword_pb2 import *
from protos.newpassword_pb2_grpc import *
from protos.notification_pb2 import *
from protos.notification_pb2_grpc import *


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
            host="shared-db-mysql-primary.default.svc.cluster.local",
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
            host="shared-db-mysql-secondary.default.svc.cluster.local",
            user="root",
            password="root",
            database="mydb",
            port="3306"
        )
        return connection
    except:
        return False


# Publish on RabbitMQ the request for a shared password. Queue request_queue
def askSharedPassword(group_name, email, service):

    pika_connection = connect_rabbitmq()
    if pika_connection != False:
        try:
            message = {'group_name':group_name, 'email':email, 'service':service}
            body = json.dumps(message)

            channel = pika_connection.channel()
            channel.exchange_declare(exchange='routing', exchange_type=ExchangeType.direct)
            channel.basic_publish(exchange='routing', routing_key='groupmanager', body=body)

            return True
        except:
            return False
        finally:
            pika_connection.close()
    else:
        return False


def storePassword(group_name, email, service, password):

    query = "INSERT INTO shared_password VALUES (%s,%s,%s,%s)"
    val = (group_name, email, service, password)

    mydb = connect_mysql_primary()
    mycursor = None

    if mydb != False:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(query,val)
            mydb.commit()
            if mycursor.rowcount > 0:
                return True
            return False
        except:
            return False
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return False


def checkIfPasswordExists(group_name, agency, email):
    
    query = "SELECT password FROM shared_password WHERE group_name = %s AND email = %s AND service = %s"
    val = (group_name, email, agency)

    mydb = connect_mysql_secondary()
    mycursor = None

    if mydb != False:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(query,val)
            myresult = mycursor.fetchall()
            if mycursor.rowcount > 0:
                return myresult[0][0]
            return None
        except:
            return None
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return None


def checkNotificationStatus(group_name, email, service):
    try:
        with grpc.insecure_channel('notification-service:50058') as channel:
            stub = NotificationStub(channel)
            response = stub.checkStatus(CheckStatusRequest(group_name=group_name, email=email, service=service))
            return response.status, response.total
    except:
        return -2, -2


def passwordCreate():
    try:
        with grpc.insecure_channel('newpw-service:50051') as channel:
            stub = PasswordStub(channel)
            response = stub.GetNewAlphaNumericPassword(NewPasswordRequest(email=None, service=None, length=8, symbols=True, hastoSave=False))
            return response.password
    except:
        return None


class Shared(SharedServicer):

    def passwordRequest(self, request, context):

        # check if password already exists ...
        password = checkIfPasswordExists(request.group_name, request.service, request.email)
        if password != None:
            return SharedPasswordReply(exists=True, password=password)

        # ... if not ...

        # ask Notification if request has already been sent
        status, total = checkNotificationStatus(request.group_name, request.email, request.service)

        # if an error occurred
        if status == -2:
            password = 'An error occurred checking your request status!'
        # if hasn't already been sent
        elif status == -1:
            # send requesto to Rabbit
            response = askSharedPassword(request.group_name, request.email, request.service)
            if response:
                password = 'Shared password requested!'
            else:
                password = 'An error occurred asking the shared password!'
        # if has been accepted
        elif status == 0:
            # send requesto to NewPassword
            password = passwordCreate()
            if password == None:
                password = 'An error occurred during the password creation!'
            else:
                # save the password on Shared-DB
                response = storePassword(request.group_name, request.email, request.service, password)
                if response:
                    return SharedPasswordReply(exists=True, password=password)
                else:
                    password = 'An error occurred saving the password!'
        # if still needs to be accepted
        else:
            # show status
            password = str(status) + '/' + str(total) + ' accepted!'

        return SharedPasswordReply(exists=False, password=password)

    def checkPassword(self, request, context):
        response = checkIfPasswordExists(request.group_name, request.agency, request.email)
        if response == request.password:
            return CheckSharedPasswordReply(isChecked=True)
        return CheckSharedPasswordReply(isChecked=False)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_SharedServicer_to_server(Shared(), server)
    server.add_insecure_port('[::]:50056')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
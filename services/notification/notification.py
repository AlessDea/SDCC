from concurrent import futures
import logging
import grpc
import mysql.connector
import pika
from pika.exchange_type import ExchangeType
import json
from email.message import EmailMessage
import ssl
import smtplib
import threading

from protos.notification_pb2 import *
from protos.notification_pb2_grpc import *
from protos.newpassword_pb2 import *
from protos.newpassword_pb2_grpc import *

file = "TokenGmail.txt"  # email_password
email_sender = 'sdccsp@gmail.com'
port = 465  # for SSL
connection = None
channel = None


def connect_rabbitmq():
    try:
        connection_parameters = pika.ConnectionParameters('rabbitmq.default.svc.cluster.local')
        pika_connection = pika.BlockingConnection(connection_parameters)
        return pika_connection
    except Exception as e:
        logging.warning('Except rabbitmq connection: ' + str(e))
        return False


def connect_mysql_primary():
    try:
        connection = mysql.connector.connect(
            host="notification-db-mysql-primary.default.svc.cluster.local",
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
            host="notification-db-mysql-secondary.default.svc.cluster.local",
            user="root",
            password="root",
            database="mydb",
            port="3306"
        )
        return connection
    except:
        return connect_mysql_primary()


def storePassword(group_name, email_applicant, service, participants, tokens):

    val = []
    for i in range(len(participants)):
        val.append(tuple([group_name, email_applicant, service, participants[i], tokens[i]]))

    mydb = connect_mysql_primary()
    mycursor = None

    if mydb != False:
        try:
            query = "INSERT INTO request VALUES (%s,%s,%s,%s,%s,'0')"
            mycursor = mydb.cursor()
            mycursor.executemany(query,val)
            mydb.commit()
            if mycursor.rowcount > 0:
                logging.warning('Store password insert ok')
                return True
            return False
        except Exception as e:
            logging.warning('Store password insert exception: ' + str(e))
            return False
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return False


def deleteRequest(group_name, email_applicant, service):

    mydb = connect_mysql_primary()
    mycursor = None

    if mydb != False:
        try:
            query = "DELETE FROM request WHERE group_name = %s AND service = %s AND email_applicant = %s"
            val = (group_name, service, email_applicant)
            mycursor = mydb.cursor()
            mycursor.execute(query, val)
            mydb.commit()
            if mycursor.rowcount > 0:
                logging.warning('DeleteRequest True')
                return True
            logging.warning('DeleteRequest False')
            return False
        except Exception as e:
            logging.warning('DeleteRequest Exception: ' + str(e))
            return False
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return False


def checkRequestStatus(group_name, email, service):

    queryStatus = "SELECT COUNT(*) FROM request WHERE group_name = %s AND email_applicant = %s AND service = %s AND status = '1'"
    queryTotal  = "SELECT COUNT(*) FROM request WHERE group_name = %s AND email_applicant = %s AND service = %s"
    val = (group_name, email, service)

    mydb = connect_mysql_secondary()
    mycursor = None

    if mydb != False:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(queryStatus,val)
            myresultStatus = mycursor.fetchall()
            mycursor.execute(queryTotal,val)
            myresultTotal = mycursor.fetchall()
            logging.warning('myResult: ' + str(myresultTotal[0][0]) + " | " + str(myresultTotal[0]))
            if myresultTotal[0][0] > 0:
                return myresultStatus[0][0], myresultTotal[0][0]
            return -1, -1
        except Exception as e:
            logging.warning("Exception: " + str(e))
            return -2, -2
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return -2, -2


def getRequestList(email):

    query  = "SELECT group_name, service, email_applicant FROM request WHERE email_member = %s AND status = '0'"
    val = (email)

    mydb = connect_mysql_secondary()
    mycursor = None

    if mydb != False:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(query,val)
            myresult = mycursor.fetchall()
            if mycursor.rowcount > 0:
                return myresult
            return []
        except:
            return None
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return None


def acceptDecline(group_name, service, email_applicant, email_member, token, accepted):

    mydb = connect_mysql_primary()
    mycursor = None

    if mydb != False:
        try:
            mycursor = mydb.cursor()

            select_query = "SELECT token FROM request WHERE group_name = %s AND service = %s AND email_applicant = %s AND email_member = %s AND status = '0'"
            val = (group_name, service, email_applicant, email_member)

            mycursor.execute(select_query, val)
            myresult = mycursor.fetchone()[0]

            if myresult == token:
                if accepted:
                    query = "UPDATE request SET status = '1' WHERE group_name = %s AND service = %s AND email_applicant = %s AND email_member = %s"
                else:
                    query = "DELETE FROM request WHERE group_name = %s AND service = %s AND email_applicant = %s"
                    val = (group_name, service, email_applicant)
                mycursor.execute(query, val)
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


def send_email(email_receiver, subject, message):
    with open(file, "r") as thefile:
        password = thefile.readlines()
    email_password = password[0].replace("\n", "")

    # Create an email
    email = EmailMessage()
    email['From'] = email_sender  # set sender
    email['To'] = email_receiver  # set receiver
    email['Subject'] = subject  # set subject
    email.set_content(message, subtype="plain", charset="utf-8")  # set body

    # Create ssl context
    context = ssl.create_default_context()
    smtp = None

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, email.as_string())
            smtp.quit()
        return True
    except Exception as e:
        logging.warning('send_email excpetion: ' + str(e))
        return False


def sendDoubleauthCode(dictionary):
    agency = dictionary['agency']
    email = dictionary['email']
    token = dictionary['token']

    subject = "Double Auth Code"

    message = "Agency: " + str(agency) + "\n\nYour Double Authentication Code is: " + str(token)

    if (send_email(email, subject, message)):
        logging.warning('Email sent')
        return True
    logging.warning('Email error')
    return False


# Consume from RabbitMQ the request from Group Manager. Queue email_queue
def on_message_received(channel, method, properties, body):

    dictionary = json.loads(body)

    logging.warning('on_message_received: ' + str(dictionary))

    if dictionary['TAG'] == 'Doubleauth':
        logging.warning('TAG Doubleauth')
        response = sendDoubleauthCode(dictionary)
        logging.warning('Control back to me')
    else:
        logging.warning('TAG SharedPassword')
        response = sendSharedPassword(dictionary)
        logging.warning('Response on_message_received: ' + str(response))

    # Send ack only if there were no errors
    # (try/except not required, at worst multiple requests are sent and only the last one is valid)
    if response:
        # Send ack when the processing is finished
        channel.basic_ack(delivery_tag=method.delivery_tag, multiple=False)
        logging.warning('Ack to rabbitmq sent')
        return True
    return False


def consumingEmailQueue():
    connection = connect_rabbitmq()
    logging.warning('Rabbitmq Connection: ' + str(connection))
    if connection != False:
        try:
            logging.warning('Connection not False')
            channel = connection.channel()
            logging.warning('Connection 1')
            channel.exchange_declare(exchange='routing', exchange_type=ExchangeType.direct)
            logging.warning('Connection 2')
            channel.queue_declare(queue='email_queue')
            logging.warning('Connection 3')
            channel.queue_bind(exchange='routing', queue='email_queue', routing_key='notification')
            logging.warning('Connection 4')
            channel.basic_qos(prefetch_count=1)   # Remove this line to let RabbitMQ act in round robin manner
            logging.warning('Connection 5')
            channel.basic_consume(queue='email_queue', on_message_callback=on_message_received)
            logging.warning('Connection 6')
            channel.start_consuming()
        except Exception as e:
            logging.warning('Rabbitmq notification Except: ' + str(e))
            return False
    else:
        return False


def sendSharedPassword(dictionary):
    group_name = dictionary['group_name']
    service = dictionary['service']
    email_applicant = dictionary['email_applicant']
    participants = dictionary['participants']

    subject = "Shared Password Request"

    logging.warning("Email shared group: " + str(group_name) + ' - Agency: ' + str(service) + ' - Applicant: ' + str(email_applicant))

    tokens = passwordCreate(len(participants))
    logging.warning('Tokens: ' + str(tokens))
    if tokens == None:
        return False

    i = 0
    for email in participants:
        message = "Group: " + str(group_name) + '\nAgency: ' + str(service) + '\nApplicant: ' + str(email_applicant) + "\n\nYour authorization code is: " + str(tokens[i]) + '\nInsert this code in the Share Password page and click on Accept or Decline'
        i = i + 1
        logging.warning('Prima di send email al partecipante')
        if not send_email(email, subject, message):
            return False
        logging.warning('Dopo di send email al partecipante')

    if storePassword(group_name, email_applicant, service, participants, tokens):
        return True
    return False


def passwordCreate(participants_number):
    tokens = []
    try:
        for _ in range(participants_number):
            with grpc.insecure_channel('newpw-service:50051') as channel:
                stub = PasswordStub(channel)
                response = stub.GetNewAlphaNumericPassword(NewPasswordRequest(email=None, service=None, length=6, symbols=False, hasToSave=False))
                tokens.append(response.password)
        return tokens
    except:
        return None


def serve():
    logging.warning('GrpcThread executing...')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_NotificationServicer_to_server(Notification(), server)
    server.add_insecure_port('[::]:50058')
    server.start()
    server.wait_for_termination()


class Notification(NotificationServicer):

    def checkStatus(self, request, context):
        status, total = checkRequestStatus(request.group_name, request.email, request.service)
        return CheckStatusReply(status=status, total=total)

    def acceptDecline(self, request, context):
        # execute accept/decline update ...
        response = acceptDecline(request.group_name, request.service, request.email_applicant, request.email_member, request.token, request.accepted)
        # ... if the accept/decline has been updated correctly ...
        if response:
            subject = "Shared Password Response"
            # ... and was a decline, send the 'Shared Password deied' email
            if request.accepted == False:
                message = 'Group: ' + str(request.group_name) + '\nAgency: ' + str(request.service) + '\n\nYour request for a Share Password has been denied by ' + str(request.email_member) + '.'
                send_email(request.email_applicant, subject, message)

            # ... and was an accept
            else:
                # check if everyone accepted and send the confirm email if so
                status, total = checkRequestStatus(request.group_name, request.email_applicant, request.service)
                if status == total:
                    message = 'Group: ' + str(request.group_name) + '\nAgency: ' + str(request.service) + '\n\nYour request for a Share Password has been accepted!'
                    send_email(request.email_applicant, subject, message)

        # returns if the accept/decline has been updated correctly
        return NotificationMessageReply(isOk=response)

    def deleteRequest(self, request, context):
        response = deleteRequest(request.group_name, request.email, request.service)
        return DeleteResponse(hasBeenDeleted=response)

    def getRequestList(self, request, context):
        response = getRequestList(request.email)
        return GetListResponse(lista=response)


if __name__ == '__main__':

    logging.basicConfig()

    logging.warning('Init notification microservice...')

    grpcThread = threading.Thread(target=serve)
    grpcThread.start()
    
    while True:
        rabbitmqThread = threading.Thread(target=consumingEmailQueue)
        rabbitmqThread.start()
        logging.warning('Rabbitmq started...')
        rabbitmqThread.join()
        logging.warning('Rabbitmq thread joined...')
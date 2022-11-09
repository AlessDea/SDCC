from concurrent import futures
import logging
import grpc
import mysql.connector
import pika
from pika.exchange_type import ExchangeType
import json
from datetime import datetime, timedelta

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
            message = {'TAG':'SharedPassword', 'group_name':group_name, 'email':email, 'service':service}
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

    if password == '':
        query = "INSERT INTO shared_password VALUES (%s,%s,%s,'','0')"
        val = (group_name, email, service)
    else:
        dt = datetime.now()
        dt = dt + timedelta(hours = 24)
        expire = datetime.timestamp(dt)
        query = "UPDATE shared_password SET password = %s, expire_date = %s WHERE group_name = %s AND email = %s AND service = %s"
        val = (password, expire, group_name, email, service)

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

    dt = datetime.now()
    now = datetime.timestamp(dt)
    
    query = "SELECT password, expire_date FROM shared_password WHERE group_name = %s AND email = %s AND service = %s"
    val = (group_name, email, agency)

    mydb = connect_mysql_secondary()
    mycursor = None

    if mydb != False:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(query,val)
            myresult = mycursor.fetchall()
            if mycursor.rowcount > 0:
                if myresult[0][0] != '':
                    if myresult[0][1] >= now:
                        return 1, myresult[0][0]    # LA PASSWORD ESISTE ED E' VALIDA
                    return 2                        # COME SE NON HA ENTRY
                return 0                            # 3 ENTRY MA PASSWORD VUOTA
            return 2                                # NON HA ENTRY
        except:
            return -1
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return -1


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


def deleteRequest(group_name, email, service):
    try:
        with grpc.insecure_channel('notification-service:50058') as channel:
            stub = NotificationStub(channel)
            response = stub.deleteRequest(DeleteRequest(group_name=group_name, email=email, service=service))
            return response.hasBeenDeleted
    except:
        return False


def deleteTransaction(group_name, email, service, password)):
    # send requesto to NewPassword
    password = passwordCreate()
    if password != None:
        # delete the request on Notification DB
        if deleteRequest(request.group_name, request.email, request.service):
            # save the password on Shared-DB
            hasBeenStored = storePassword(request.group_name, request.email, request.service, password)
            if hasBeenStored:
                return True, f"{group_name}: Your Shared Password for the service {service} is: {password}"
            return False, 'An error occurred storing the password!'
        return False, 'An error occurred deleting the accepted request!'
    return False, 'An error occurred during the password creation!'


class Shared(SharedServicer):

    def passwordRequest(self, request, context):
        # check if password already exists and isn't expired ...
        result, password = checkIfPasswordExists(request.group_name, request.service, request.email)
        # ... if an error occurred
        if result == -1:
            password = 'An error occurred checking your password!'
        # ... if entry exists but password is empty
        elif result == 0:
            response, password = deleteTransaction(request.group_name, request.email, request.service)
            return SharedPasswordReply(exists=response, password=password)
        # ... if exists and it's valid
        elif result == 1:
            return SharedPasswordReply(exists=True, password=password)
        # ... if not ...
        else:
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
                    password = f"{group_name}: Your Shared Password for the service {service} has been requested!"
                else:
                    password = 'An error occurred asking the shared password!'
            # if has been accepted
            elif status == 0:
                storeRequest = storePassword(request.group_name, request.email, request.service, '')
                if storeRequest:
                    # delete the request on Notification DB and store the password
                    response, password = deleteTransaction(request.group_name, request.email, request.service)
                    return SharedPasswordReply(exists=response, password=password)
                password = 'An error occurred storing the entry'
            # if still needs to be accepted
            else:
                # show status
                password = str(status) + ' out of ' + str(total) + ' users has accepted!'

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
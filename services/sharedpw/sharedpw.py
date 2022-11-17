from concurrent import futures
import logging
import grpc
import mysql.connector
import pika
import threading
from pika.exchange_type import ExchangeType
import json
from datetime import datetime, timedelta

from protos.sharedpw_pb2 import *
from protos.sharedpw_pb2_grpc import *
from protos.newpassword_pb2 import *
from protos.newpassword_pb2_grpc import *

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
        return connect_mysql_primary()


# Publish on RabbitMQ the request for member's list from Group Manager. Queue request_queue
def publishForGroupManager(message):

    connection = connect_rabbitmq()
    if connection != False:
        try:
            body = json.dumps(message)
            channel = connection.channel()
            channel.exchange_declare(exchange='routing', exchange_type=ExchangeType.direct, durable=True)
            channel.basic_publish(exchange='routing', routing_key='groupmanager', body=body, properties=pika.BasicProperties(delivery_mode=2,))
            connection.close()
            return True
        except:
            return False
    else:
        return False


def publishForNotification(message):
    connection = connect_rabbitmq()
    if connection != False:
        try:
            body = json.dumps(message)
            channel = connection.channel()
            channel.exchange_declare(exchange='routing', exchange_type=ExchangeType.direct, durable=True)
            channel.basic_publish(exchange='routing', routing_key='notification', body=body, properties=pika.BasicProperties(delivery_mode=2,))
            connection.close()
            return True
        except:
            return False
    else:
        return False


def storePassword(group_name, email, service, password):

    expire = str(datetime.now() + timedelta(hours=24))
    logging.warning('expire: ' + str(len(expire)))
    queryUpdate = "UPDATE shared SET password = %s, expire_date = %s WHERE group_name = %s AND email_applicant = %s AND service = %s"
    queryDelete = "DELETE FROM request WHERE shared_group_name = %s AND shared_service = %s AND shared_email_applicant = %s"
    valUpdate = (password, expire, group_name, email, service)
    valDelete = (group_name, service, email)

    mydb = connect_mysql_primary()
    mycursor = None

    if mydb != False:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(queryUpdate,valUpdate)
            if mycursor.rowcount > 0:
                mycursor.execute(queryDelete,valDelete)
                mydb.commit()
                if mycursor.rowcount > 0:
                    return True             # Update password e cancellazione richieste
            return False
        except Exception as e:
            logging.warning('Store password Exception: ' + str(e))
            mydb.rollback()
            return False
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return False


def checkIfPasswordExists(group_name, agency, email):

    now = datetime.now()
    
    query = "SELECT password, expire_date FROM shared WHERE group_name = %s AND service = %s AND email_applicant = %s"
    queryShared = "INSERT INTO shared VALUES (%s,%s,%s,'','')"
    val = (group_name, agency, email)

    mydb = connect_mysql_secondary()
    mycursor = None

    if mydb != False:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(query,val)
            myresult = mycursor.fetchall()
            if mycursor.rowcount > 0:
                if myresult[0][0] != '':
                    expire = datetime.strptime(myresult[0][1],"%Y-%m-%d %H:%M:%S.%f")
                    if expire >= now:
                        return 1, myresult[0][0]    # LA PASSWORD ESISTE ED E' VALIDA
                return 0, None                      # LA PASSWORD ESISTE MA E' SCADUTA OR PASSWORD VUOTA
            mycursor.execute(queryShared, val)
            mydb.commit()
            if mycursor.rowcount > 0:
                return 0, None                      # NESSUNA ENTRY                   
            return -1, None
        except Exception as e:
            logging.warning('CheckIfPasswordExists: ' + str(e))
            return -1, None
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return -1, None


def checkRequestStatus(group_name, email, service):
    
    queryStatus = "SELECT COUNT(*) FROM request WHERE shared_group_name = %s AND shared_email_applicant = %s AND shared_service = %s AND status = '1'"
    queryTotal  = "SELECT COUNT(*) FROM request WHERE shared_group_name = %s AND shared_email_applicant = %s AND shared_service = %s"
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
            return -1, -1                               # Nessuna entry presente
        except Exception as e:
            logging.warning("Exception: " + str(e))
            return -2, -2                               # Errore
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return -2, -2                                   # Errore


def passwordCreate():
    try:
        with grpc.insecure_channel('newpw-service:50051') as channel:
            stub = PasswordStub(channel)
            response = stub.GetNewAlphaNumericPassword(NewPasswordRequest(email=None, service=None, length=8, symbols=True, hasToSave=False))
            return response.password
    except:
        raise Exception


def generateTokens(participants_number):
    tokens = []
    try:
        for _ in range(participants_number):
            with grpc.insecure_channel('newpw-service:50051') as channel:
                stub = PasswordStub(channel)
                response = stub.GetNewAlphaNumericPassword(NewPasswordRequest(email=None, service=None, length=6, symbols=False, hasToSave=False))
                tokens.append(response.password)
        return tokens
    except:
        raise Exception


def saveRequests(group_name, email_applicant, service, participants, tokens):

    val = []
    for i in range(len(participants)):
        val.append(tuple([group_name, service, email_applicant, participants[i], tokens[i]]))

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


def acceptDecline(group_name, service, email_applicant, email_member, token, accepted):

    mydb = connect_mysql_primary()
    mycursor = None

    if mydb != False:
        try:
            mycursor = mydb.cursor()

            select_query = "SELECT token FROM request WHERE shared_group_name = %s AND shared_service = %s AND shared_email_applicant = %s AND email_member = %s AND status = '0'"
            val = (group_name, service, email_applicant, email_member)

            mycursor.execute(select_query, val)
            myresult = mycursor.fetchone()[0]

            if myresult == token:
                if accepted:
                    query = "UPDATE request SET status = '1' WHERE shared_group_name = %s AND shared_service = %s AND shared_email_applicant = %s AND email_member = %s"
                else:
                    query = "DELETE FROM request WHERE shared_group_name = %s AND shared_service = %s AND shared_email_applicant = %s"
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


def getRequestList(email):

    query  = "SELECT shared_group_name, shared_service, shared_email_applicant FROM request WHERE email_member = %s AND status = '0'"
    val = (email,)

    mydb = connect_mysql_secondary()
    mycursor = None

    if mydb != False:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(query,val)
            myresult = mycursor.fetchall()
            if mycursor.rowcount > 0:
                logging.warning('myresult getrequestlist: ' + str(myresult))
                return myresult
            return []
        except Exception as e:
            logging.warning('GetRequestList db exception: ' + str(e))
            return None
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return None


class Shared(SharedServicer):

    def passwordRequest(self, request, context):
        logging.warning('Entrato in PasswordRequest ' + str(request.group_name) + str(request.service) + str(request.email))
        # check if password already exists and isn't expired
        result, password = checkIfPasswordExists(request.group_name, request.service, request.email)
        logging.warning('Result ' + str(result) + ' | Password: ' + str(password))

        # ... if an error occurred
        if result == -1:
            password = 'An error occurred checking your password!'
         
        # ... if password exists and is valid
        elif result == 1:
            password = f"{request.group_name} - Your Shared Password for the service {request.service} is: {password}"
            return SharedPasswordReply(exists=True, password=password)

        # ... if password is empty or not valid or doesn't exist
        else:
            logging.warning("Entrato nell'else di PassRequest")
            # check if request has already been sent
            status, total = checkRequestStatus(request.group_name, request.email, request.service)
            logging.warning('Status: ' + str(status) + " | Total: " + str(total))

            # if an error occurred
            if status == -2:
                password = 'An error occurred checking your request status!'

            # if hasn't already been sent
            elif status == -1:
                logging.warning('Invio una nuova richiesta')
                # send request to Rabbit
                message = {'group_name':request.group_name, 'email':request.email, 'service':request.service}
                response = publishForGroupManager(message)
                logging.warning('Rabbitmq resp: ' + str(response))
                if response:
                    password = f"{request.group_name} - Your Shared Password for the service {request.service} has been requested!"
                else:
                    password = 'An error occurred asking the shared password!'
                    logging.warning('Rabbitmq unreachable...')

            # if has been accepted
            elif (total - status) == 0:
                # send requesto to NewPassword
                try:
                    password = passwordCreate()
                    # save the password on Shared-DB
                    hasBeenStored = storePassword(request.group_name, request.email, request.service, password)
                    if hasBeenStored:
                        return SharedPasswordReply(exists=True, password=f"{request.group_name} - Your Shared Password for the service {request.service} is: {password}")
                    else: #???
                        #return SharedPasswordReply(exists=False, password='An error occurred storing the password!')
                        raise Exception
                except:
                    raise Exception
                #return SharedPasswordReply(exists=False, password='An error occurred during the password creation!')

            # if still needs to be accepted
            else:
                # show status
                password = str(status) + ' out of ' + str(total) + ' users has accepted!'

        logging.warning('Messaggio di reply: ' + str(password))
        return SharedPasswordReply(exists=False, password=password)

    def checkPassword(self, request, context):
        response, password = checkIfPasswordExists(request.group_name, request.agency, request.email)
        if (response == 1) and (password == request.password):
            logging.warning('Response: ' + str(response) + ' | Password: ' + str(password))
            return CheckSharedPasswordReply(isChecked=True)
        return CheckSharedPasswordReply(isChecked=False)

    def acceptDecline(self, request, context):
        # execute accept/decline update ...
        response = acceptDecline(request.group_name, request.service, request.email_applicant, request.email_member, request.token, request.accepted)
        # ... if the accept/decline has been updated correctly ...
        if response:

            # Pubblica il messaggio su Rabbitmq per Notification
            message = {'TAG':'AcceptDecline', 'accepted':str(request.accepted), 'group_name':request.group_name, 'email_applicant': request.email_applicant, 'service':request.service, 'email_member':request.email_member}

            # ... and was a decline, send the 'Shared Password denied' email
            if request.accepted == False:
                # Publish Rabbitmq invio email di risposta 
                logging.warning('Declined --> Publish on rabbitmq')
                publishForNotification(message)

            # ... and was an accept
            else:
                # check if everyone accepted and send the confirm email if so
                status, total = checkRequestStatus(request.group_name, request.email_applicant, request.service)
                if status == total:
                    # Publish Rabbitmq invio email di risposta 
                    logging.warning('Accepted --> Publish on rabbitmq')
                    publishForNotification(message)
                    # send requesto to NewPassword
                    try:
                        password = passwordCreate()
                        # save the password on Shared-DB (non controlliamo errore, verrà generata quando cliccherà il pulsante get shared password in caso di errore)
                        storePassword(request.group_name, request.email_applicant, request.service, password)
                    except:
                        raise Exception

        # returns if the accept/decline has been updated correctly
        return NotificationMessageReply(isOk=response)

    def getRequestList(self, request, context):
        response = getRequestList(request.email)
        
        lista = []
        for e in response:
            lista.append(Result(group_name=e[0], agency=e[1], applicant=e[2]))
        return GetListResponse(lista=lista)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_SharedServicer_to_server(Shared(), server)
    server.add_insecure_port('[::]:50056')
    server.start()
    server.wait_for_termination()


# Consume from RabbitMQ the info from Group Manager. Queue info_queue
def on_message_received(channel, method, properties, body):

    dictionary = json.loads(body)
    group_name = dictionary['group_name']
    service = dictionary['service']
    email_applicant = dictionary['email_applicant']
    participants = dictionary['participants']

    logging.warning('on_message_received - Group: ' + str(group_name) + " Email_applicant: " + str(email_applicant) + " Service: " + str(service) + " list: " + str(participants))
    
    # Generazione token 
    try:
        tokens = generateTokens(len(participants))
        logging.warning('Tokens: ' + str(tokens))
    except:
        return False #non lancio eccezione in modo che il thread consumingInfoQueue non venga tirato giù

    # Salvataggio richieste nel db
    if saveRequests(group_name, email_applicant, service, participants, tokens):
        # Pubblica su Rabbitmq il messaggio per notification
        message = {'TAG':'SharedPassword', 'group_name':group_name, 'email_applicant':email_applicant, 'service':service, 'participants':participants, 'tokens':tokens} 
        if publishForNotification(message):
            # Send ack only if there were no errors
            # (try/except not required, at worst multiple requests are sent and only the last one is valid)
            channel.basic_ack(delivery_tag=method.delivery_tag, multiple=False)
            logging.warning('Rabbitmq groupmanager ack sent')
            return True
    return False


def consumingInfoQueue():
    connection = connect_rabbitmq()
    logging.warning('Rabbitmq connection: ' + str(connection))
    if connection != False:
        try:
            channel = connection.channel()
            logging.warning('Rabbitmq connection 1')
            channel.exchange_declare(exchange='routing', exchange_type=ExchangeType.direct, durable=True)
            logging.warning('Rabbitmq connection: 2')
            channel.queue_declare(queue='info_queue', durable=True)
            logging.warning('Rabbitmq connection: 3')
            channel.queue_bind(exchange='routing', queue='info_queue', routing_key='sharedpassword')
            logging.warning('Rabbitmq connection: 4')
            channel.basic_qos(prefetch_count=1)   # Remove this line to let RabbitMQ act in round robin manner
            logging.warning('Rabbitmq connection: 5')
            channel.basic_consume(queue='info_queue', on_message_callback=on_message_received)
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
        rabbitmqThread = threading.Thread(target=consumingInfoQueue)
        logging.warning('\n\n\nAvvio thread rabbitmq')
        rabbitmqThread.start()
        rabbitmqThread.join()
        logging.warning('Join thread rabbitmq')

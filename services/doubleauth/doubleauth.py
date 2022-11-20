from concurrent import futures

import grpc
import mysql.connector
import logging
import json
import pika
from pika.exchange_type import ExchangeType

from protos.newpassword_pb2 import *
from protos.newpassword_pb2_grpc import *
from protos.doubleauth_pb2_grpc import *
from protos.doubleauth_pb2 import *

from lib.breaker_listeners import *

breaker = pybreaker.CircuitBreaker(fail_max=2, reset_timeout=5, listeners=[GreetingsListener(), LogListener()])

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
            host="doubleauth-db-mysql-primary.default.svc.cluster.local",
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
            host="doubleauth-db-mysql-secondary.default.svc.cluster.local",
            user="root",
            password="root",
            database="mydb",
            port="3306"
        )
        return connection
    except:
        return connect_mysql_primary()


def registerThirdPart(email, agency):

    query = "INSERT INTO doubleauth VALUES (%s,%s,'')"
    val = (email, agency)

    mydb = connect_mysql_primary()
    mycursor = None

    if mydb != False:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(query,val)
            mydb.commit()
            if mycursor.rowcount > 0:
                return True             # Registrazione andata a buon fine
            return False                # Registrazione fallita o utente già registrato
        except:
            return False                # Registrazione fallita o utente già registrato
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return False                    # Registrazione fallita o utente già registrato


def loginThirdPart(email, agency):

    queryCheckLogin = "SELECT * FROM doubleauth WHERE email = %s AND agency = %s"
    val = (email,agency)
    queryUpdateCode = "UPDATE doubleauth SET token = %s WHERE email = %s AND agency = %s"
    
    mydb = connect_mysql_primary()
    mycursor = None

    if mydb != False:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(queryCheckLogin,val)
            mycursor.fetchall()
            if mycursor.rowcount > 0:                               # Coppia agenzia-email esistente --> genera il token 
                code = generateCode(email)
                if code != None:
                    val = (code,email,agency)
                    mycursor.execute(queryUpdateCode,val)
                    mydb.commit()
                    if mycursor.rowcount > 0:
                        if (sendMessage(email, agency, code)):      # Tutto è andato bene, torna True per comunicare al sito di terze parti di indirizzare l'utente sulla pagina di doppia autenticazione
                            logging.warning('SendMessage True')
                            return True
                        logging.warning('SendMessage False')
            return False                                            # Errore generico o coppia agenzia-email non esistente
        except:
           raise Exception                                          # Errore generico o coppia agenzia-email non esistente
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return False                                                # Errore generico o coppia agenzia-email non esistente


def sendMessage(email, agency, code):

    message = {"TAG":"Doubleauth", "email":email, "agency":agency, "token":code}
    packet = json.dumps(message)
    
    connection = connect_rabbitmq()
    logging.warning('Rabbitmq Connection: ' + str(connection))
    if connection != False:
        try:
            channel = connection.channel()
            channel.exchange_declare(exchange='routing', exchange_type=ExchangeType.direct, durable=True)
            channel.basic_publish(exchange='routing', routing_key='notification', body=packet, properties=pika.BasicProperties(delivery_mode=2,))
            connection.close()
            logging.warning('Rabbitmq Ok')
            return True
        except:
            logging.warning('Rabbitmq Except')
            return False
    return False

@breaker
def generateCode(email):
    try:
        with grpc.insecure_channel('newpw-service:50051') as channel:
            stub = PasswordStub(channel)
            response = stub.GetNewNumericPassword(NewPasswordRequest(email=email, length=5, service=None, symbols=False, hasToSave=False))
            return response.password
    except:
        raise Exception


def checkDoubleAuthCode(email, agency, code):

    query = "SELECT token FROM doubleauth WHERE email = %s AND agency = %s"
    val = (email, agency)

    logging.warning('Connessione al DB')
    mydb = connect_mysql_secondary()
    logging.warning('mydb: ' + str(mydb))
    mycursor = None

    if mydb != False:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(query,val)
            myresult = mycursor.fetchall()
            if mycursor.rowcount > 0 and myresult[0][0] == code:
                logging.warning('DB and code tutto ok')
                return True                                 # Codice corretto
            logging.warning('DB and code errato')
            return False                                    # Codice errato o errore generico
        except:
            logging.warning('DB error')
            return False                                    # Codice errato o errore generico
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return False                                        # Codice errato o errore generico


class Doubleauth(DoubleauthServicer):

    # +--------------------------------------------------------------------------------+
    # | Registra un nuovo utente per i siti di terze parti                             |
    # |  -> ritorna un booleano che indica se la richiesta è andata a buon fine o meno |
    # +--------------------------------------------------------------------------------+
    def registrationThirdPart(self, request, context):
        response = registerThirdPart(request.email, request.service)
        return Reply(message=response)

    # +--------------------------------------------------------------------------------------------------------------------------------------+
    # | Effettua il login per i siti di terze parti, richiede la generazione del codice di doppia autenticazione e richede l'invio via email |
    # |  -> ritorna un booleano che indica se la richiesta è andata a buon fine o meno                                                       |
    # +--------------------------------------------------------------------------------------------------------------------------------------+
    def doLoginThirdPart(self, request, context):
        logging.warning('Login Third entered - ' + str(request.email) + str(request.service))
        response = loginThirdPart(request.email, request.service)
        logging.warning('Login Third return ' + str(response))
        return Reply(message=response)

    # +--------------------------------------------------------------------------------+
    # | Effettua il controllo del codice di doppia autenticazione                      |
    # |  -> ritorna un booleano che indica se la richiesta è andata a buon fine o meno |
    # +--------------------------------------------------------------------------------+
    def checkCode(self, request, context):
        logging.warning('Check Code entered')
        response = checkDoubleAuthCode(request.email, request.service, request.code)
        logging.warning('Check Code return ' + str(response))
        return Reply(message=response)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_DoubleauthServicer_to_server(Doubleauth(), server)
    server.add_insecure_port('[::]:50059')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
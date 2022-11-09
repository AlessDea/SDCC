import grpc
import mysql.connector
import logging
import json
import pika
from pika.exchange_type import ExchangeType

from protos.newpassword_pb2 import *
from protos.newpassword_pb2_grpc import *


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
        return False


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
                return True # Registrazione andata a buon fine
            return False # Registrazione fallita o utente già registrato
        except:
            return False # Registrazione fallita o utente già registrato
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return False # Registrazione fallita o utente già registrato


def loginThirdPart(email, agency):

    queryCheckLogin = "SELECT * FROM doubleauth where email = %s AND agency = %s"
    val = (email,agency)
    queryUpdateCode = "UPDATE doubleauth SET token = %s WHERE email = %s AND agency = %s"
    
    mydb = connect_mysql_primary()
    mycursor = None

    if mydb != False:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(queryCheckLogin,val)
            mycursor.fetchall()
            if mycursor.rowcount > 0: # Coppia agenzia-email esistente --> genera il token 
                code = generateCode(email)
                if code != None:
                    val = (code,email,agency)
                    mycursor.execute(queryUpdateCode,val)
                    mydb.commit()
                    if mycursor.rowcount > 0:
                        if (sendMessage(email, agency, code)): # Tutto è andato bene, torna True per comunicare al sito di terze parti di indirizzare l'utente sulla pagina di doppia autenticazione
                            return True
            return False # Errore generico o coppia agenzia-email non esistente
        except:
            return False # Errore generico o coppia agenzia-email non esistente
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return False # Errore generico o coppia agenzia-email non esistente


def sendMessage(email, agency, code):

    message = {"TAG":"Doubleauth", "email":email, "agency":agency, "token":code}
    packet = json.dumps(message)
  
    connection = connect_rabbitmq()
    if connection:
        try:
            channel = connection.channel()
            channel.exchange_declare(exchange='routing', exchange_type=ExchangeType.direct)
            channel.basic_publish(exchange='routing', routing_key='notification', body=packet)
            connection.close()
            return True
        except:
            return False
    return False


def generateCode(email):
    try:
        with grpc.insecure_channel('newpw-service:50051') as channel:
            stub = PasswordStub(channel)
            response = stub.GetNewNumericPassword(NewPasswordRequest(email=email, length=5, service=None, symbols=False, hasToSave=False))
            return response.password
    except:
        return None


def checkDoubleAuthCode(email, agency, code):

    query = "SELECT token FROM user where email = %s AND agency = %s"
    val = (email, agency, code)

    mydb = connect_mysql_secondary()
    mycursor = None

    if mydb != False:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(query,val)
            myresult = mycursor.fetchall()
            if mycursor.rowcount > 0 and myresult[0][0] == code:
                return True # Codice corretto
            return False # Codice errato o errore generico
        except:
            return False # Codice errato o errore generico
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return False # Codice errato o errore generico


class Doubleauth(DoubleauthServicer):

    def registrationThirdPart(self, request, context):
        response = registerThirdPart(request.email, request.agency)
        return RegistrationReply(isRegistered=response)

    def doLoginThirdPart(self, request, context):
        response = loginThirdPart(request.email, request.agency)
        return LoginReply(isLogged=response)

    def checkCode(self, request, context):
        response = checkDoubleAuthCode(request.email, request.agency, request.code)
        return LoginReply(isLogged=response)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_DoubleauthServicer_to_server(Doubleauth(), server)
    server.add_insecure_port('[::]:50059')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
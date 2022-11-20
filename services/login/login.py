from concurrent import futures
import logging
import grpc
import mysql.connector

from protos.login_pb2 import *
from protos.login_pb2_grpc import *


def connect_mysql_primary():
    try:
        connection = mysql.connector.connect(
            host="login-db-mysql-primary.default.svc.cluster.local",
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
            host="login-db-mysql-secondary.default.svc.cluster.local",
            user="root",
            password="root",
            database="mydb",
            port="3306"
        )
        return connection
    except:
        return connect_mysql_primary()


def register(name, password, isAgency):

    if isAgency == True:
        query = "INSERT INTO agency VALUES (%s,%s)"
        val = (name, password)
    else:
        query = "INSERT INTO user VALUES (%s,%s)"
        val = (name, password)

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


def login(name, password, isAgency):

    if isAgency == True:
        query = "SELECT password FROM agency where name = %s"
    else:
        query = "SELECT password FROM user where email = %s"

    mydb = connect_mysql_secondary()
    mycursor = None

    if mydb != False:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(query,(name,))
            myresult = mycursor.fetchall()
            if mycursor.rowcount > 0 and myresult[0][0] == password:
                if isAgency == False:
                    query = "SELECT COUNT(*) FROM user_agency WHERE user_email = %s"
                    mycursor.execute(query,(name,))
                    myresult = mycursor.fetchall()
                    if myresult[0][0] > 0:
                        return 2 # Utente loggato e facente parte di un'agenzia
                return 1 # Utente non appartenente ad un'agenzia oppure un'agenzia loggata
            return 0 # Credenziali errate
        except:
            return -1 # Errore generico
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return -1 # Errore generico


def checkEmployee(email, agency):
    
    query = "SELECT COUNT(*) FROM user WHERE email = %s"
    mydb = connect_mysql_secondary()
    mycursor = None

    if mydb != False:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(query,(email,))
            myresult = mycursor.fetchall()
            if myresult[0][0] > 0: # L'utente esiste
                query = "SELECT COUNT(*) FROM user_agency WHERE user_email = %s AND agency_name = %s"
                val = (email, agency)
                mycursor.execute(query,val)
                myresult = mycursor.fetchall()
                if myresult[0][0] > 0: # L'utente è nell'agenzia
                    return 0
                return 1 # L'utente non è nell'agenzia
            return 2 # L'utente non esiste
        except:
            return -1 # Altro errore generico
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return -1 # Altro errore generico

    
def addEmployee(email, agency):
    
    query = "INSERT INTO user_agency VALUES (%s,%s)"
    val = (email, agency)

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


def checkAgency(agency):
    query = "SELECT COUNT(*) FROM agency WHERE name = %s"
    mydb = connect_mysql_secondary()
    mycursor = None

    if mydb != False:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(query,(agency,))
            myresult = mycursor.fetchall()
            if myresult[0][0] > 0: # L'agenzia esiste
                return True
            return False # L'agenzia non esiste
        except:
            return False # Altro errore generico
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return False # Altro errore generico


class Login(LoginServicer):

    # +-------------------------------------------------------------------------------+
    # | Effettua la registrazione di un utente o di un'agenzia                        |
    # |  -> ritorna un booleano che indica se la richesta è andata a buon fine o meno |
    # +-------------------------------------------------------------------------------+
    def registration(self, request, context):
        response = register(request.username, request.password, request.isAgency)
        return RegistrationReply(isRegistered=response)

    # +-------------------------------------------------------------------------------+
    # | Effettua il login di un utente o di un'agenzia                                |
    # |  -> ritorna un booleano che indica se la richesta è andata a buon fine o meno |
    # +-------------------------------------------------------------------------------+
    def doLogin(self, request, context):
        response = login(request.username, request.password, request.isAgency)
        return LoginReply(isLogged=response)

    # +----------------------------------------------------------------------+
    # | Controlla se un utente è dipendete di un'agenzia                     |
    # |  -> ritorna un booleano che indica se l'utente è un dipendete o meno |
    # +----------------------------------------------------------------------+
    def checkEmployee(self, request, context):
        response = checkEmployee(request.email, request.agency)
        return CheckEmployeeReply(isEmployeeChecked=response)

    # +-------------------------------------------------------------------------------+
    # | Aggiunge un utente alla lista dei dipendeti per un'agenzia                    |
    # |  -> ritorna un booleano che indica se la richesta è andata a buon fine o meno |
    # +-------------------------------------------------------------------------------+
    def addEmployee(self, request, context):
        response = addEmployee(request.email, request.agency)
        return AddEmployeeReply(isEmployeeAdded=response)

    # +---------------------------------------------------------------------+
    # | Controlla se un'agenzia è registrata nella piattaforma              |
    # |  -> ritorna un booleano che indica se l'agenzia è registrata o meno |
    # +---------------------------------------------------------------------+
    def checkAgency(self, request, context):
        response = checkAgency(request.agency)
        return CheckAgencyReply(isAgencyChecked=response)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_LoginServicer_to_server(Login(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
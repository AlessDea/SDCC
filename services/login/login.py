from concurrent import futures
import logging
import grpc
from mysql.connector import Error

from protos.login_pb2 import *
from protos.login_pb2_grpc import *
from protos.newpassword_pb2 import *
from protos.newpassword_pb2_grpc import *
from protos.savepwd_pb2 import *
from protos.savepwd_pb2_grpc import *
from protos.register_pb2 import *
from protos.register_pb2_grpc import *
from protos.listing_pb2 import *
from protos.listing_pb2_grpc import *
import mysql.connector

def connect_mysql():
    try:
        connection = mysql.connector.connect(
            host="login-db",
            # host='localhost',
            user="root",
            password="",
            database="mydb"
            # port="3306",
            # auth_plugin='mysql_native_password'
        )
        return connection
    except:
        return False


def login(name, pssw, isAgency):

    if isAgency == True:
        query = "SELECT password FROM user where username = %s and isAgency = 1"
    else:
        query = "SELECT password FROM user where username = %s and isAgency = 0"

    mydb = connect_mysql()

    if mydb != False:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(query,(name,))
            myresult = mycursor.fetchall()
            if mycursor.rowcount > 0 and myresult[0][0] == pssw:
                return True
            return False
        except:
            return False
        finally:
            mycursor.close()
    else:
        return False


def getMail(name):

    query = "SELECT email FROM user where username = %s"

    mydb = connect_mysql()

    if mydb != False:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(query,(name,))
            myresult = mycursor.fetchall()
            if mycursor.rowcount > 0:
                return myresult[0][0]
            return False
        except:
            return False
        finally:
            mycursor.close()
    else:
        return False


class Login(LoginServicer):

    def doLogin(self, request, context):
        response = login(request.username, request.password, request.type)
        return LogReply(isLogged=response)

    def getEmail(self, request, context):
        response = getMail(request.username)
        return EmailReply(email=response)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_LoginServicer_to_server(Login(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
from concurrent import futures
import logging
import grpc
from mysql.connector import Error

import login_pb2
import login_pb2_grpc
import mysql.connector

def connect_mysql():
    connection = mysql.connector.connect(
        host="login-db",
        # host='localhost',
        user="root",
        password="password",
        database="mydb",
        port="3306",
        auth_plugin='mysql_native_password'
    )
    return connection


def login(name, pssw, isAgency):

    if isAgency == True:
        query = "SELECT password FROM agencies where username = %s"
    else:
        query = "SELECT password FROM user where username = %s"

    mydb = connect_mysql()

    mycursor = mydb.cursor()
    try:
        mycursor.execute(query,(name,))
        myresult = mycursor.fetchall()
        if mycursor.rowcount > 0 and myresult[0][0] == pssw:
            return True
        return False
    finally:
        mycursor.close()


def getMail(name):

    query = "SELECT email FROM user where username = %s"

    mydb = connect_mysql()

    mycursor = mydb.cursor()
    try:
        mycursor.execute(query,(name,))
        myresult = mycursor.fetchall()
        if mycursor.rowcount > 0:
            return myresult[0][0]
        return False
    finally:
        mycursor.close()


class Login(login_pb2_grpc.LoginServicer):

    def doLogin(self, request, context):
        response = login(request.username, request.password, request.type)
        return login_pb2.LogReply(isLogged=response)

    def getEmail(self, request, context):
        response = getMail(request.username)
        return login_pb2.EmailReply(email=response)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    login_pb2_grpc.add_LoginServicer_to_server(Login(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
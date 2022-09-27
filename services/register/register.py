from concurrent import futures
import logging
import grpc
from mysql.connector import Error

import register_pb2
import register_pb2_grpc
import mysql.connector

def connect_mysql():
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


def register(name, pssw, email):

    if email == "":
        query = "INSERT INTO agencies VALUES (%s,%s)"
        val = (name, pssw)
    else:
        query = "INSERT INTO user VALUES (%s,%s,%s)"
        val = (name, email, pssw)

    mydb = connect_mysql()

    mycursor = mydb.cursor()
    try:
        mycursor.execute(query,val)
        mydb.commit()
        if mycursor.rowcount > 0:
            return True
        return False
    except:
        return False
    finally:
        mycursor.close()


class Register(register_pb2_grpc.RegisterServicer):

    def registration(self, request, context):
        response = register(request.username, request.password, request.email)
        return register_pb2.PwReply(isRegistered=response)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    register_pb2_grpc.add_RegisterServicer_to_server(Register(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
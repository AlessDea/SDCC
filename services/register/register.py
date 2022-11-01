from concurrent import futures
import logging
import grpc

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
            host="user-db-mysql-primary.default.svc.cluster.local",
            user="root",
            password="root",
            database="userdb",
            port="3306"
        )
        return connection
    except:
        return False


def register(name, pssw, email):

    if email == "":
        query = "INSERT INTO user VALUES (%s,'',%s,1)"
        val = (name, pssw)
    else:
        query = "INSERT INTO user VALUES (%s,%s,%s,0)"
        val = (name, email, pssw)

    mydb = connect_mysql()

    if mydb != False:
        try:
            mydb = connect_mysql()
            mycursor = mydb.cursor()
            mycursor.execute(query,val)
            mydb.commit()
            if mycursor.rowcount > 0:
                return True
            return False
        except:
            return False
        finally:
            mycursor.close()
    else:
        return False


class Register(RegisterServicer):

    def registration(self, request, context):
        response = register(request.username, request.password, request.email)
        return RegReply(isRegistered=response)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_RegisterServicer_to_server(Register(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
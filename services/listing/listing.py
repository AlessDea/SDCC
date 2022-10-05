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
            host="private-password-db",
            user="root",
            password="",
            database="mydb"
        )
        return connection
    except:
        return False


def listing(name):
    services   = []
    passwords  = []
    dictionary = {}

    query = "SELECT service, password FROM private_passwords where username = %s"

    mydb = connect_mysql()

    if mydb != False:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(query,(name,))
            myresult = mycursor.fetchall()
            for i in range (0, mycursor.rowcount):
                services.append(myresult[i][0])
                passwords.append(myresult[i][1])
            dictionary = dict(zip(services, passwords))
            if mycursor.rowcount > 0 and myresult[0][0] == pssw:
                return dictionary
            return dictionary
        except:
            return dictionary
        finally:
            mycursor.close()
    else:
        return dictionary


class Listing(ListingServicer):

    def doList(self, request, context):
        response = listing(request.username)
        return ListReply(list=response)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_ListingServicer_to_server(Listing(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
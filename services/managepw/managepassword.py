from concurrent import futures
import logging
import grpc
import mysql.connector

from protos.managepassword_pb2 import *
from protos.managepassword_pb2_grpc import *


def connect_mysql_primary():
    try:
        connection = mysql.connector.connect(
            host="private-db-mysql-primary.default.svc.cluster.local",
            user="root",
            password="root",
            database="mydb"
        )
        return connection
    except:
        return False


def connect_mysql_secondary():
    try:
        connection = mysql.connector.connect(
            host="private-db-mysql-secondary.default.svc.cluster.local",
            user="root",
            password="root",
            database="mydb"
        )
        return connection
    except:
        return False


def save(email, password, service):

    mydb = connect_mysql_primary()
    mycursor = None

    if mydb != False:
        try:
            mycursor = mydb.cursor()

            check_query = "SELECT COUNT(*) FROM private_passwords WHERE email = %s AND service = %s"
            val = (email, service)
            mycursor.execute(check_query, val)
            myresult = mycursor.fetchone()[0]

            if (myresult == 0):
                query1 = 'INSERT INTO private_passwords VALUES (%s, %s, %s)'
                val = (email, service, password)
                mycursor.execute(query1, val)
            else:
                query2 = "UPDATE private_passwords SET password = %s WHERE email = %s AND service = %s"
                val = (password, email, service)
                mycursor.execute(query2, val)

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

def listing(name):
    services   = []
    passwords  = []
    dictionary = {}

    query = "SELECT service, password FROM private_passwords WHERE email = %s"

    mydb = connect_mysql_secondary()
    mycursor = None

    if mydb != False:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(query,(name,))
            myresult = mycursor.fetchall()
            for i in range (0, mycursor.rowcount):
                services.append(myresult[i][0])
                passwords.append(myresult[i][1])
            dictionary = dict(zip(services, passwords))
            return dictionary
        except:
            return dictionary
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return dictionary


class Saver(SaverServicer):

    def SavePassword(self, request, context):
        response = save(request.email, request.password, request.service)
        return SavePasswordReply(isStored=response)

    def doList(self, request, context):
        response = listing(request.email)
        return ListPasswordReply(list=response)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_SaverServicer_to_server(Saver(), server)
    server.add_insecure_port('[::]:50054')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
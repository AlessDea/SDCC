from concurrent import futures
import logging
import grpc
from mysql.connector import Error

import savepwd_pb2
import savepwd_pb2_grpc
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

def save(uname, pw, service):

    mydb = connect_mysql()

    if mydb != False:

        try:
            mycursor = mydb.cursor()

            check_query = "SELECT COUNT(*) FROM private_passwords WHERE username = %s AND service = %s"
            val = (uname, service)
            mycursor.execute(check_query, val)
            myresult = mycursor.fetchone()[0]

            if (myresult == 0):
                query1 = 'INSERT INTO private_passwords VALUES (%s, %s, %s)'
                val = (uname, service, pw)
                mycursor.execute(query1, val)
            else:
                query2 = "UPDATE private_passwords SET password = %s WHERE username = %s AND service = %s"
                val = (pw, uname, service)
                mycursor.execute(query2, val)

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


class Saver(savepwd_pb2_grpc.SaverServicer):

    def SavePw(self, request, context):
        response = save(request.username, request.pw, request.service)
        return savepwd_pb2.SaveReply(isStored=response)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    savepwd_pb2_grpc.add_SaverServicer_to_server(Saver(), server)
    server.add_insecure_port('[::]:50054')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
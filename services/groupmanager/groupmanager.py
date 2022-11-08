from concurrent import futures
import logging
import grpc

from protos.login_pb2 import *
from protos.login_pb2_grpc import *
from protos.groupmanager_pb2_grpc import *
from protos.groupmanager_pb2 import *

import mysql.connector


def connect_mysql_primary():
    try:
        connection = mysql.connector.connect(
            host="group-db-mysql-primary.default.svc.cluster.local",
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
            host="group-db-mysql-secondary.default.svc.cluster.local",
            user="root",
            password="root",
            database="mydb",
            port="3306"
        )
        return connection
    except:
        return False


def groupCreate(group_name, emails, agency):

    mydb = connect_mysql_primary()
    mycursor = None

    val = []

    for email in emails:
        val.append(tuple([group_name, email, agency]))

    if mydb != False:
        try:
            query = "INSERT INTO team VALUES (%s,%s,%s)"
            mycursor = mydb.cursor()
            mycursor.executemany(query,val)
            mydb.commit()
            if mycursor.rowcount > 0:
                return 0
            return -1
        except:
            return -1
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return -1


def groupList(email):
    group_names  = []
    services     = []
    dictionary   = {}

    query = "SELECT group_name, service FROM team WHERE email = %s"

    mydb = connect_mysql_secondary()
    mycursor = None

    if mydb != False:
        try:
            mycursor = mydb.cursor()
            mycursor.execute(query,(email,))
            myresult = mycursor.fetchall()
            for i in range (0, mycursor.rowcount):
                group_names.append(myresult[i][0])
                services.append(myresult[i][1])
            dictionary = dict(zip(group_names, services))
            return dictionary
        except:
            return dictionary
        finally:
            if mycursor != None:
                mycursor.close()
    else:
        return dictionary


def checkUserAgency(emails, agency):

    for email in emails:
        try:
            with grpc.insecure_channel('login-service:50052') as channel:
                stub = LoginStub(channel)
                response = stub.checkEmployee(CheckEmployeeRequest(email=email, agency=agency))

                if response.isEmployeeChecked != 0:
                    return response.isEmployeeChecked       # può ritornare -1, 1, 2
        except:
            return -1
    return response.isEmployeeChecked                       # ritorna 0


class GroupManager(GroupManagerServicer):

    def groupCreate(self, request, context):

        check = checkUserAgency(request.emails, request.agency)

        if check == 0:
            response = groupCreate(request.group_name, request.emails, request.agency)
            return GroupCreateReply(isCreated=response)
        return GroupCreateReply(isCreated=check)

    def groupList(self, request, context):
        response = groupList(request.email)

        # BISOGNA CHIAMARE PSW_CONDIVISA PER SAPERE SE HO UNA PASSWORD PER OGNI GRUPPO

        return GroupListReply(list=response)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_GroupManagerServicer_to_server(GroupManager(), server)
    server.add_insecure_port('[::]:50057')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
import grpc
import pika
import time
import logging
import json
import sys
from concurrent import futures

import pymongo
from pymongo import MongoClient


from protos.sharedpw_pb2 import *
from protos.sharedpw_pb2_grpc import *

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

def sharePwReq(gid, user):

    message = {gid : user}
    packet = json.dumps(message)

    # Use the default channel
    channel = connection.channel()

    # Declare the queue, create if needed
    channel.queue_declare(queue='request_queue')

    # Use the default exchange
    # message = f"Sending messageId: {messageId}"
    channel.basic_publish(exchange='', routing_key='request_queue', body=packet)
    print(f"sent message: {packet}")

    # Close connection
    connection.close()
    return True




def sharedPwResp(gid, res, tkn, user):
    ''' bisogna implementare il controllo sul db della richiesta '''
    # Connect client to the MongoDB
    client = MongoClient('mongodb://localhost:27017')
    # Chose db
    db = client.grouprequests
    # Connect to the collection, creates it if doesn't exist.
    usersRespCollection = db.usersResp

    if res == 'ACCEPTED':
        # Query
        result = usersRespCollection.find({"groupId": gid, "participants.username": user}).limit(1)
        participants = []
        for user in result:
            participants.append(user.get("participants"))

        i = 0
        p = None
        for p in participants:
            if p[0].get("username") == user:
                break
            i = i + 1

        token = p[i].get("token")
        if token == tkn:
            result = usersRespCollection.update_one({"groupId": gid, "participants.username": user}, {"$set": {"participants.$.accepted": True}})

        acceptedFlag = True
        for p in participants:
            if p['accepted'] == False:
                acceptedFlag = False

        if acceptedFlag == True:
            # chiama il microservizio newpw e fatti generare una nuova password

            # invia la nuova password a group manager

            # cancella dal database le entry delle richieste per questo gruppo
            usersRespCollection.delete_one({"groupId": gid})

    else: #vuol dire che la richiesta è stata rifiutata, quindi eliminala dal db
        usersRespCollection.delete_one({"groupId": gid})


def registrateInfo(groupId, creator, users, tokens, agency):
    # Connect client to the MongoDB
    client = MongoClient('mongodb://localhost:27017')
    # Chose db
    db = client.grouprequests
    # Connect to the collection, creates it if doesn't exist.
    usersRespCollection = db.usersResp

    newGroup = {}
    newGroup["groupId"] = int(groupId)
    newGroup["creator"] = creator
    newGroup["participants"] = []
    i = 0
    for user in users:
        elem = {}
        elem["username"] = user
        elem["token"] = tokens[i]
        elem["accepted"] = False
        i = i + 1
        newGroup["participants"].append(elem)
    newGroup["agency"] = agency

    result = usersRespCollection.insert_one(newGroup)
    print(newGroup)


class Shared(SharedServicer):
    def makeReq(self, request, context):
        ret = sharePwReq(request.groupId, request.username)
        return ShReply(message=str(ret))


    def sendResp(self, request, context):
        ret = sharedPwResp(int(request.groupId), request.result, request.token, request.username)
        return respRep(message=str(ret))

    def sendInfo(self, request, context):
        ret = registrateInfo(request.groupId, request.creator, request.username, request.token, request.extra)
        return InfoResp(message=str(ret))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_SharedServicer_to_server(server)
    server.add_insecure_port('[::]:50056')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
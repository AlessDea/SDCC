import grpc
import pika
import time
import logging
import json
import sys
from concurrent import futures


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


def registrateInfo():
    ''' prende le informazioni del gruppo che gli arrivano da group manager e le scrive
        sul suo db. Le informazioni sono:
        - username/email di tutti gli utenti
        - id del gruppo
        - token di tutti glit utenti
        Usiamo Mongo
     '''

class Shared(SharedServicer):
    def makeReq(self, request, context):
        ret = sharePwReq(request.groupId, request.username)
        return ShReply(message=str(ret))


    def sendResp(self, request, context):
        ret = sharedPwResp(request.groupId, request.result, request.token, request.username)
        return respRep(message=str(ret))

    def sendInfo(self, request, context):
        ret = registrateInfo()
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
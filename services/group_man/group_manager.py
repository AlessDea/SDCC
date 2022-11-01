# questo sarebbe il servizio di password condivise: prende le richieste e le 
# inoltra al microservizio per l'invio delle email, prende poi le risposte dei singoli utenti
from concurrent import futures

import pika
import time
import random
import json
import threading

import db_utils

from protos.sharedpw_pb2 import *
from protos.sharedpw_pb2_grpc import *
from protos.newpassword_pb2 import *
from protos.newpassword_pb2_grpc import *
from protos.gp_manager_pb2 import *
from protos.gp_manager_pb2_grpc import *

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)



class GpCreator(GpCreatorServicer):
   def gpCreate(self, request, context):
        response = db_utils.create_group(request.group_name, request.username, request.email, request.service)
        return gpCreateRep(isCreated=response)



def create_group_thread():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_GpCreatorServicer_to_server(GpCreator(), server)
    server.add_insecure_port('[::]:50057')
    server.start()
    server.wait_for_termination()



def get_participants(group_id):
    emails_lst = db_utils.get_emails()  # restituisce la lista di email
    return  emails_lst


def tokens_generations(n):
    tokens = []
    for e in range(n):
        with grpc.insecure_channel('newpw-service:50051') as channel:
            stub = PasswordStub(channel)
            response = stub.GetNewNumPass(PwRequest(name=None, length=6, service=None, symbols=False, hastoSave=False))

            tokens.append(response.pw)
    return tokens


def produce_req(group_id, emails, tkns):
    print('sending email to group ', group_id)

    message = dict.fromkeys(emails)

    for e, t in emails, tkns:
        message[e] = t + "@" + str(group_id)

    packet = json.dumps(message)

    channel = connection.channel()

    # Declare the queue, create if needed
    channel.queue_declare(queue='emails_queue')

    # Use the default exchange
    # message = f"Sending messageId: {messageId}"
    channel.basic_publish(exchange='', routing_key='emails_queue', body=packet)
    #print(f"sent message: {packet}")
    # Close connection
    #connection.close()


def on_message_received(channel, method, properties, body):

    '''
        invia le informazioni al microservizio shared_pw
    '''


    info_lst = db_utils.get_info(json.loads(body))
    usernames = []
    emails_lst = []
    for r in info_lst:
        usernames.append(r[1])
        emails_lst.append(r[2])


    gid = info_lst[0][0]
    agency = info_lst[0][3]
    tkns = tokens_generations(len(emails_lst))


    with grpc.insecure_channel('sharedpw-service:50056') as channel:
        stub = SharedStub(channel)
        info = InfoMsg()
        info.groupId.append(gid)
        info.username.extend(usernames)
        info.token.extend(tkns)
        info.creator.append(None)
        info.extra.append(agency)
        response = stub.sendInfo(info)

    print(f"received: {json.loads(body)}")

    produce_req(json.loads(body), emails_lst, tkns)

    # Send ack when the processing is finished
    channel.basic_ack(delivery_tag=method.delivery_tag)
    print("Finished processing the message")


if __name__ == '__main__':

    groupCreatorThr = threading.Thread(target=create_group_thread())
    groupCreatorThr.start()

    # Use the default channel
    channel = connection.channel()
    # Declare the queue, create if needed
    channel.queue_declare(queue='request_queue')

    # Set prefetch count, a consumer can only process one message at a time
    # Comment this line to test the RabbitMQ acts in round robin manner
    # channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue='request_queue', on_message_callback=on_message_received)

    print("starting consumer")
    channel.start_consuming()

    groupCreatorThr.join()

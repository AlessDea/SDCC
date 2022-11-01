# questo sarebbe il servizio di password condivise: prende le richieste e le 
# inoltra al microservizio per l'invio delle email, prende poi le risposte dei singoli utenti
import pika
import time
import random
import json

import db_utils

from protos.sharedpw_pb2 import *
from protos.sharedpw_pb2_grpc import *
from protos.newpassword_pb2 import *
from protos.newpassword_pb2_grpc import *

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)




def produce_req(group_id):
    '''
    bisogna anche generare dei token, quindi qui deve chiedere al microservizio newpw di generarli per lui
    poi li mette insieme alle email e li invia
    '''
    print('sending email to group ', group_id)

    emails_lst = db_utils.get_emails() #restituisce la lista di email
    num_t = len(emails_lst) #numero di token da generare

    message = dict.fromkeys(emails_lst)
    #chiama newpw e genera un token per ogni email
    for e in emails_lst:
        with grpc.insecure_channel('newpw-service:50051') as channel:
            stub = PasswordStub(channel)
            response = stub.GetNewNumPass(PwRequest(name=None, length=6, service=None, symbols=False, hastoSave=False))
            message[e] = str(response) + "@" + str(group_id)


    packet = json.dumps(message)
    # while True:
    # Use the default channel

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
        fai una lettura su db delle informazioni:
        - groupId
        - usernames: lista dei partecipanti al gruppo
        - tokens: lista dei tokens generati
        - creator: creatore del gruppo
        - ex: per informazioni extra
    '''

    with grpc.insecure_channel('shared-pw:50056') as channel:
        stub = SharedStub(channel)
        response = stub.sendInfo(InfoMsg(groupId = gid, username=usernames, token = tokens, creator=creator, extra=ex))



    print(f"received: {json.loads(body)}")

    produce_req(json.loads(body))

    # Send ack when the processing is finished
    channel.basic_ack(delivery_tag=method.delivery_tag)
    print("Finished processing the message")


if __name__ == '__main__':
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

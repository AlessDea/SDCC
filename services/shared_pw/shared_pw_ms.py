import pika
import time
import random
import json
import sys

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

def run():
    # if json.loads(body)['type'] == 'req':
    #     produce_req(json.loads(body)['gid'])
    # else:
    #    if json.loads(body)['acceptans'] == 'yes':
    #        print('Requeste has been accepted by ', json.loads(body)['username'])
    #    else:
    #        print('Requeste has not been accepted by ', json.loads(body)['username'])

    grpcReq = "req"     #richiesta arrivata tramite grpc

    if grpcReq == 'req':
        message = {'req': grpcReq}
        packet = json.dumps(message)

        # Use the default channel
        channel = connection.channel()

        # Declare the queue, create if needed
        channel.queue_declare(queue='request_queue')

        # Use the default exchange
        # message = f"Sending messageId: {messageId}"
        channel.basic_publish(exchange='', routing_key='request_queue', body=packet)
        print(f"sent message: {packet}")
    elif sys.argv[1] == 'resp':
        print('è un messaggio di risposta ad una richiesta e bisogna quindi contarla')

    # Close connection
    connection.close()


if __name__ == '__main__':
    run()
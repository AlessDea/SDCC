# questo sarebbe il servizio di password condivise: prende le richieste e le 
# inoltra al microservizio per l'invio delle email, prende poi le risposte dei singoli utenti
import pika
import time
import random
import json

import db_utils
from send_email import send_email

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)




def produce_req(group_id):

    print('sending email to group ', group_id)
    #message = ["alessandro.deangelis.97@students.uniroma2.eu", "ale.flanker97@gmail.com", "alessandro.deangelis97@gmail.com"]

    message = db_utils.get_emails()
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

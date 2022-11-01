import pika
import time
import random
import json
from send_email import send_email

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)


def on_message_received(channel, method, properties, body):
    # print(f"received: {json.loads(body)}, will take {processing_time} to process...")
    d = json.loads(body)
    for e in d:
        #print(e)
        send_email(e, d[e])

    # Simulate processing

    # Send ack when the processing is finished
    channel.basic_ack(delivery_tag=method.delivery_tag)
    print("Finished processing the message")


if __name__ == '__main__':
    # Use the default channel
    channel = connection.channel()
    # Declare the queue, create if needed
    channel.queue_declare(queue='emails_queue')

    # Set prefetch count, a consumer can only process one message at a time
    # Comment this line to test the RabbitMQ acts in round robin manner
    # channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue='emails_queue', on_message_callback=on_message_received)

    print("starting consumer")
    channel.start_consuming()

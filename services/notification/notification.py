import logging
import pika
from pika.exchange_type import ExchangeType
import json
from email.message import EmailMessage
import ssl
import smtplib

file = "TokenGmail.txt"  # email_password
email_sender = 'sdccsp@gmail.com'
port = 465  # for SSL
connection = None
channel = None


def connect_rabbitmq():
    try:
        connection_parameters = pika.ConnectionParameters('rabbitmq.default.svc.cluster.local')
        pika_connection = pika.BlockingConnection(connection_parameters)
        return pika_connection
    except Exception as e:
        logging.warning('Except rabbitmq connection: ' + str(e))
        return False


def sendEmail(email_receiver, subject, message):
    with open(file, "r") as thefile:
        password = thefile.readlines()
    email_password = password[0].replace("\n", "")

    # Create an email
    email = EmailMessage()
    email['From'] = email_sender  # set sender
    email['To'] = email_receiver  # set receiver
    email['Subject'] = subject  # set subject
    email.set_content(message, subtype="plain", charset="utf-8")  # set body

    # Create ssl context
    context = ssl.create_default_context()
    smtp = None

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, email.as_string())
            smtp.quit()
        return True
    except Exception as e:
        logging.warning('send_email excpetion: ' + str(e))
        return False


def sendDoubleauthCode(dictionary):
    agency = dictionary['agency']
    email = dictionary['email']
    token = dictionary['token']

    subject = "Double Auth Code"

    message = "Agency: " + str(agency) + "\n\nYour Double Authentication Code is: " + str(token)

    if (sendEmail(email, subject, message)):
        logging.warning('Email sent')
        return True
    logging.warning('Email error')
    return False


def sendSharedPassword(dictionary):
    group_name = dictionary['group_name']
    service = dictionary['service']
    email_applicant = dictionary['email_applicant']
    participants = dictionary['participants']
    tokens = dictionary['tokens']
    
    subject = "Shared Password Request"

    logging.warning("Email shared group: " + str(group_name) + ' - Agency: ' + str(service) + ' - Applicant: ' + str(email_applicant) + ' - Tokens: ' + str(tokens))

    i = 0
    for email in participants:
        message = "Group: " + str(group_name) + '\nAgency: ' + str(service) + '\nApplicant: ' + str(email_applicant) + "\n\nYour authorization code is: " + str(tokens[i]) + '\n\nInsert this code in the Share Password page and click on Accept or Decline'
        i = i + 1
        logging.warning('Prima di send email al partecipante')
        if not sendEmail(email, subject, message):
            return False
        logging.warning('Dopo di send email al partecipante')

    return True


def sendAcceptDecline(dictionary):
    group_name = dictionary['group_name']
    service = dictionary['service']
    email_applicant = dictionary['email_applicant']
    email_member = dictionary['email_member']
    accepted = dictionary['accepted']
    
    subject = "Shared Password Response"

    if accepted == 'True':
        message = 'Group: ' + str(group_name) + '\nAgency: ' + str(service) + '\n\nYour request for a Share Password has been accepted!'
        logging.warning('Prima di send email')
        if not sendEmail(email_applicant, subject, message):
            return False
        logging.warning('Dopo di send email')
    else:
        message = 'Group: ' + str(group_name) + '\nAgency: ' + str(service) + '\n\nYour request for a Share Password has been denied by ' + str(email_member) + '.'
        logging.warning('Prima di send email')
        if not sendEmail(email_applicant, subject, message):
            return False
        logging.warning('Dopo di send email')

    return True


def consumingEmailQueue():
    connection = connect_rabbitmq()
    logging.warning('Rabbitmq Connection: ' + str(connection))
    if connection != False:
        try:
            logging.warning('Connection not False')
            channel = connection.channel()
            logging.warning('Connection 1')
            channel.exchange_declare(exchange='routing', exchange_type=ExchangeType.direct)
            logging.warning('Connection 2')
            channel.queue_declare(queue='email_queue')
            logging.warning('Connection 3')
            channel.queue_bind(exchange='routing', queue='email_queue', routing_key='notification')
            logging.warning('Connection 4')
            channel.basic_qos(prefetch_count=1)   # Remove this line to let RabbitMQ act in round robin manner
            logging.warning('Connection 5')
            channel.basic_consume(queue='email_queue', on_message_callback=on_message_received)
            logging.warning('Connection 6')
            channel.start_consuming()
        except Exception as e:
            logging.warning('Rabbitmq notification Except: ' + str(e))
            return False
    else:
        return False


# Consume from RabbitMQ the request from Group Manager. Queue email_queue
def on_message_received(channel, method, properties, body):

    dictionary = json.loads(body)

    logging.warning('on_message_received: ' + str(dictionary))

    if dictionary['TAG'] == 'Doubleauth':
        logging.warning('TAG Doubleauth')
        response = sendDoubleauthCode(dictionary)
        logging.warning('Control back to me')
    elif dictionary['TAG'] == 'AcceptDecline':
        logging.warning('TAG AcceptDecline')
        response = sendAcceptDecline(dictionary)
        logging.warning('Response on_message_received: ' + str(response))
    else:
        logging.warning('TAG SharedPassword')
        response = sendSharedPassword(dictionary)
        logging.warning('Response on_message_received: ' + str(response))

    # Send ack only if there were no errors
    # (try/except not required, at worst multiple requests are sent and only the last one is valid)
    if response:
        # Send ack when the processing is finished
        channel.basic_ack(delivery_tag=method.delivery_tag, multiple=False)
        logging.warning('Ack to rabbitmq sent')
        return True
    return False


if __name__ == '__main__':

    logging.basicConfig()
    logging.warning('Init Notification microservice...')

    while True:
        consumingEmailQueue()
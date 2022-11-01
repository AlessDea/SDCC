"""
 Automate Emails with Python using Gmail account
"""
import random
from email.message import EmailMessage
import ssl
import smtplib

file = "TokenGmail.txt"  # email_password = "ldqdlcuuugaijjvy"
email_sender = 'sdccsp@gmail.com'
port = 465  # for SSL


def send_email(email_receiver, t):
    with open(file, "r") as thefile:
        password = thefile.readlines()
    email_password = password[0].replace("\n", "")

    print("\nSending email...\n")

    # Set subject and body of the email
    subject = "Share password Request - Group: " +  t.split('@') [1]
    body = "Your authorization code is: " + t.split('@') [0] + \
           "\nInsert this code in the Share Password page ad click on Accept or Decline"

    # Create an email
    email = EmailMessage()
    email['From'] = email_sender  # set sender
    email['To'] = email_receiver  # set receiver
    email['Subject'] = subject  # set subject
    email.set_content(body, subtype="plain", charset="utf-8")  # set body

    # Create ssl context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, email.as_string())
        smtp.quit()

    print("Email sent to " + email_receiver + "\n")

# if __name__ == '__main__':

# with open(file, "r") as thefile:
#       password = thefile.readlines()
# email_password = password[0].replace("\n","")

# send_email("donatello.d@tiscali.it", email_password)
# send_email("donatello.d1973@libero.it", email_password)
# send_email("cecco.pol@libero.it", email_password)
# send_email("spazianipierpaolo@tiscali.com", email_password)

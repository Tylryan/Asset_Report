#!/usr/bin/python

from email.message import EmailMessage
import smtplib
import os
import sys

sys.path.insert(
    0, '/home/tyler/Documents/Coding/Stock-Report/Stock-Report/Functions')
my_email = 'tlrrn5@gmail.com'


def send_email(to):
    from read_config import export_variables
    password, crypto_api = export_variables(
        env_location='/home/tyler/Documents/Coding/Stock-Report/Data/.env')
    print(password)
    message = EmailMessage()
    message['subject'] = "Testing 1 2 3"
    message['from'] = my_email
    message['to'] = to
    message.set_content('What does this do?')
    html_message = open(
        '/home/tyler/Documents/Coding/Stock-Report/Stock-Report/Functions/Email/report.html').read()
    html_message.close()
    message.add_alternative(html_message, subtype='html')
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(my_email, password)
        smtp.send_message(message)


send_email(my_email)

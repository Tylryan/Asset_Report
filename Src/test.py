#!/usr/bin/python3

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


username = 'tlrrn5@gmail.com'

password = 'qtlcaehqfzdxxrln'


def send_mail(

        text="Email Body",
        subject="Hello World",
        from_email=username,
        to_emails=username
):
    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = to_emails
    msg['Subject'] = subject

    txt_part = MIMEText(text, 'plain')
    msg.attach(txt_part)

    html_part = MIMEText(
        f"""
<h2> This is working<h2>
<p> Let's see if I can send a formatted string inside of this html.
Alright here we go. 

Can you see {text} that?</p>


            """, "html")
    msg.attach(html_part)

    msg_string = msg.as_string()

    server = smtplib.SMTP(
        host='smtp.gmail.com',
        port=587
    )
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(from_email, to_emails, msg_string)

    server.quit()


send_mail()

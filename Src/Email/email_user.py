#!/usr/bin/python3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd

from read_config import export_variables
from data_analysis import stock_report


username, password = export_variables()


def send_mail(

        # report,
        text="Email Body",
        subject="Stock/Crypto Report",
        from_email=username,
        to_emails=username
):
    msg = MIMEMultipart('related')
    msg['From'] = from_email
    msg['To'] = to_emails
    msg['Subject'] = subject

    msg.add_alternative(report_html, subtype='html')

    txt_part = MIMEText(text, 'plain')
    msg.attach(txt_part)

    html_part = MIMEText(
        f"""
<html>
    <head></head>
    <body>
        <h2>Your Daily Stock Report<h2>
        <p> Here is a list of some stocks that are below their 200 day moving average:</p>
        {report}
        <img src = "./Email/stock_image.png">
    </body>
</html>
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
    server.sendmail(from_email, to_emails, msg.as_string())

    server.quit()


if __name__ == "__main__":
    send_mail()

#!/usr/bin/python
# from read_config import export_variables
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
import sys

sys.path.append('../')


def send_email(email, password):
    msg = MIMEMultipart()

    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = 'Stock Report'

    body = """
    <html>
        <head></head>
        <body>
            <h1>Stock/Crypto Report</h1>
            <p>This stock/crypto triggered this email.</p>
            <img src="cid:img1"
            <img src="cid:img2"
            style = "width:250px;">
        </body>
    </html>

    """
    msg.attach(MIMEText(body, "html"))

    file_image = open(
        './Functions/Email/stock_image1.png', 'rb')
    file_image2 = open(
        './Functions/Email/stock_image2.png', 'rb')
    email_image = MIMEImage(file_image.read())
    email_image2 = MIMEImage(file_image2.read())
    file_image.close()
    file_image2.close()

    email_image.add_header("Content-ID", "<image1>")
    email_image2.add_header("Content-ID", "<image2>")
    msg.attach(email_image)
    msg.attach(email_image2)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, msg.as_string())
    server.quit()

    return 0


if __name__ == '__main__':
    # send_email()
    pass

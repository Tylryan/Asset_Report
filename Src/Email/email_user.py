#!/usr/bin/python3

from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import smtplib
import sys


class Email():
    def report(self):
        """
        The report that will be emailed if no exceptions are raised.

        Keeping track of Crypto:        True
        Stocks to buy:                  True
        Cryptocurrencies to buy:        True
        """
        msg = MIMEMultipart()
        msg['Subject'] = "Caught A Bite!"
        msg['From'] = self.email_address
        msg['To'] = self.email_address

        html = """\
        <html>
          <head></head>
          <body>
            <h1>Your Daily Asset Report is Ready!!!</h1>
            <h2>Stocks Ready For The Pickings!</h2>
            {0}
            <h2>Cryptocurrencies On Sale Today!</h2>
            {1}
            <h2>Other Stocks You Are Keeping Track Of</h2>
            {2}
            <h2>Other Cryptocurrencies You Are Keeping Track Of</h2>
            {3}
          </body>
        </html>
        """.format(
            self.buy_stock_df.to_html(),
            self.buy_crypto_df.to_html(),
            self.do_not_buy_stock_df.to_html(),
            self.do_not_buy_crypto_df.to_html()
        )

        part1 = MIMEText(html, 'html')
        msg.attach(part1)

        server = smtplib.SMTP(
            host='smtp.gmail.com',
            port=587
        )
        server.ehlo()
        server.starttls()
        server.login(self.email_address, self.password)
        server.sendmail(
            self.email_address,
            self.email_address,
            msg.as_string()
        )

        server.quit()

    def report2(self):
        """
        The report that will be emailed if there are no buys and the user is keeping track of crypto currencies.

        Keeping track of crypto:         True
        Stocks to buy:                   False
        Cryptocurrencies to buy:         False
        """
        msg = MIMEMultipart()
        msg['Subject'] = "No Buy Opportunities"
        msg['From'] = self.email_address
        msg['To'] = self.email_address

        html = """\
        <html>
          <head></head>
          <body>
            <h1>No Buy Opportunities Today</h1>
            <h3>However, here are a list of stocks and cryptocurrencies in order by how close their current price is to their 252 day moving average</h3>
            <h2>Stocks To Look Out For</h2>
            <br>
            {0}
            <br>
            <h2>Cryptocurrencies To Look Out For</h2>
            {1}
            <br>
          </body>
        </html>
        """.format(
            self.do_not_buy_stock_df.to_html(),
            self.do_not_buy_crypto_df.to_html()
        )

        part1 = MIMEText(html, 'html')
        msg.attach(part1)

        server = smtplib.SMTP(
            host='smtp.gmail.com',
            port=587
        )
        server.ehlo()
        server.starttls()
        server.login(self.email_address, self.password)
        server.sendmail(
            self.email_address,
            self.email_address,
            msg.as_string()
        )
        server.quit()

    def report3(self):
        """
        The report that will be emailed if the user is not keeping track of Crypto and there are stocks to buy

        Keeping track of crypto:         False
        Stocks to buy:                   True
        """
        msg = MIMEMultipart()
        msg['Subject'] = "Stock Buy Opportunities"
        msg['From'] = self.email_address
        msg['To'] = self.email_address

        html = """\
        <html>
          <head></head>
          <body>
            <h1>Buy Opportunities of the Day</h1>
            {0}
            <br>
            <h2>Stocks To Look Out For</h2>
            <br>
            {1}
            <br>
          </body>
        </html>
        """.format(
            self.buy_stock_df.to_html(),
            self.do_not_buy_stock_df.to_html()
        )

        part1 = MIMEText(html, 'html')
        msg.attach(part1)

        server = smtplib.SMTP(
            host='smtp.gmail.com',
            port=587
        )
        server.ehlo()
        server.starttls()
        server.login(self.email_address, self.password)
        server.sendmail(
            self.email_address,
            self.email_address,
            msg.as_string()
        )
        server.quit()

    def report4(self):
        """
        The report that will be emailed if the user is not keeping track of Crypto and there are no stocks to buy

        Keeping track of crypto:         False
        Stocks to buy:                   False
        """
        msg = MIMEMultipart()
        msg['Subject'] = "No Buy Opportunities"
        msg['From'] = self.email_address
        msg['To'] = self.email_address

        html = """\
        <html>
          <head></head>
          <body>
            <h2>Unfortunately there are no buy opportunities today.</h2>
            <h3>Here are some stocks that could be close to becoming an opportunity.</h1>
            {0}
            <br>
          </body>
        </html>
        """.format(
            self.do_not_buy_stock_df.to_html()
        )

        part1 = MIMEText(html, 'html')
        msg.attach(part1)

        server = smtplib.SMTP(
            host='smtp.gmail.com',
            port=587
        )
        server.ehlo()
        server.starttls()
        server.login(self.email_address, self.password)
        server.sendmail(
            self.email_address,
            self.email_address,
            msg.as_string()
        )
        server.quit()


if __name__ == "__main__":
    pass

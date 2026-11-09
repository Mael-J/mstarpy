from mstarpy import Funds, Stock


from mstarpy.security import Security
import datetime
import pandas as pd
from mstarpy.search import MorningstarSession
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os



def send_email(subject, body):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587


    sender = os.environ["EMAIL"]
    password = os.environ["EMAIL_PASSWORD"]
    recipient = os.environ["EMAIL"]


    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject


    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(message)


def test_all_function():
    """ test all function and send a email in case there is a problem"""
    session = MorningstarSession()

    fund = Funds("FR0011351659", session=session)
    #print(fund.maxDrawDown())
    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(30)
    try:
        nav = fund.nav(start_date,end_date)
        #send valied email with checkbox valid
        send_email("✅ mstarpy", "Fund NAV is valid.")
    except Exception as e:
        send_email("❌ Error in fund.nav", str(e))
        return






if __name__ == "__main__":

    test_all_function()























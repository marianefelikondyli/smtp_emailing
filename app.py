from flask import Flask
import smtplib

import os
import sys

from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate


app = Flask(__name__)


def send_email_with_attachment(subject, body_text, to_emails, file_to_attach):
    """
         Send an email with an attachment
         """
    base_path = os.path.dirname(os.path.abspath(__file__))
    header = 'Content-Disposition', f'attachment; filename={file_to_attach}'
    print(header)

    host = "prometheus.uphellas.gr"
    from_addr = "bi@uphellas.gr"

    # create the message
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    if body_text:
        msg.attach(MIMEText(body_text))

    msg["To"] = to_emails

    attachment = MIMEBase('application', "octet-stream")
    try:
        with open(file_to_attach, "rb") as fh:
            data = fh.read()
        attachment.set_payload(data)
        encoders.encode_base64(attachment)
        attachment.add_header(*header)
        msg.attach(attachment)
    except IOError:
        msg = f"Error opening attachment file {file_to_attach}"
        print(msg)
        sys.exit(1)

    server = smtplib.SMTP(host)
    server.sendmail(from_addr, to_emails, msg.as_string())
    server.quit()
    return "Email sent"



@app.route('/')
def send_basic_email():
    host = "prometheus.uphellas.gr"
    server = smtplib.SMTP(host)
    FROM = "bi@uphellas.gr"
    TO = "nefeli.kondyli@uphellas.gr"
    MSG = "Subject: LALALALALAL\n\nStavros sucks!!"
    server.sendmail(FROM, TO, MSG)
    server.quit()
    return "Email Send"


@app.route('/send_email')
def send_email():
    resp = send_email_with_attachment("My test email", "Here is your body", "nefeli.kondyli@uphellas.gr",
                                      "./files/uninvoiced_2024-1-29_2024-2-29.xlsx")
    return resp

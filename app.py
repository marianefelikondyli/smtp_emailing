from flask import Flask, Response
import smtplib
import os
import sys
from configparser import ConfigParser
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate


app = Flask(__name__)


HOST = "lala.server.com"
SUBJECT = "my subject"
TO = "nefeli.kondyli@uphellas.gr"
FROM = "lala@mydomain.com"
text = "Text of the email"
FILE = "C:\\Users\\nefeli.kondyli\\Data Projects\\uninvoiced\\uninvoiced_2022-9-12_2022-9-26.xlsx"

BODY = "\r\n".join((
    "From: %s" % FROM,
    "To: %s" % TO,
    "Subject: %s" % SUBJECT,
    "",
    text
    ))


def send_email_with_attachment(subject, body_text, to_emails, file_to_attach):
    """
    Send an email with an attachment
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, "email.ini")
    header = 'Content-Disposition', 'attachment; filename="%s"' % file_to_attach

    # get the config
    if os.path.exists(config_path):
        cfg = ConfigParser()
        cfg.read(config_path)
    else:
        print("Config not found! Exiting!")
        sys.exit(1)

    # extract server and from_addr from config
    host = cfg.get("smtp", "server")
    from_addr = cfg.get("smtp", "from_addr")

    # create the message
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    if body_text:
        msg.attach( MIMEText(body_text) )

    msg["To"] = ', '.join(to_emails)

    attachment = MIMEBase('application', "octet-stream")
    try:
        with open(file_to_attach, "rb") as fh:
            data = fh.read()
        attachment.set_payload(data)
        encoders.encode_base64(attachment)
        attachment.add_header(*header)
        msg.attach(attachment)
    except IOError:
        msg = "Error opening attachment file %s" % file_to_attach
        print(msg)
        sys.exit(1)

    server = smtplib.SMTP(host)
    server.sendmail(from_addr, to_emails, msg.as_string())
    server.quit()


@app.route('/', methods=['POST', 'GET'])
def hello():
    server = smtplib.SMTP(HOST)
    server.sendmail(FROM, [TO], BODY)
    server.quit()


@app.route('/test', methods=['POST', 'GET'])
def test():
    send_email_with_attachment(subject=SUBJECT, body_text=text, to_emails="nefeli.kondyli@uphellas.gr",
                               file_to_attach=FILE)


if __name__ == "__main__":
    app.run(debug=True)

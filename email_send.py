import smtplib
import ssl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SENDER = 'info@ingo-janssen.de'
PASSWORD = input('E-Mail Account Passwort eingeben: ')
SMTP_SERVER = 'smtp.ionos.de'
SMTP_PORT = 465

RECIPIENT = ['info@ingo-janssen.de', 'ingo.m.janssen@gmail.com']
SUBJECT = 'Ein netter Gruß.'
MESSAGE_TEXT = '''Guten Morgen!
Ich wünsche dir einen wunderschönen Tag!'''
MESSAGE_HTML = '''
<html>
    <body>
        <p>Guten Morgen!</p>
        <p>Ich wünsche dir einen wunderschönen Tag!</p>
        <p>Schau doch mal auf meiner <a href="https://ingo-janssen.de">Webseite</a> vorbei</p>
    </body>
</html>
'''
ATTACHMENT = 'README.md'


def send_text_email():
    # needed for SSL usage - requires certificates
    # context = ssl.create_default_context()
    # with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as mail_server:
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as mail_server:
        mail_server.login(SENDER, PASSWORD)
        mail_server.sendmail(SENDER, RECIPIENT, MESSAGE_TEXT.encode('utf-8'))


def send_html_email():
    message = MIMEMultipart('alternative')
    message['Subject'] = SUBJECT
    message['From'] = SENDER
    message['To'] = ','.join(RECIPIENT)

    message_content_plain = MIMEText(MESSAGE_TEXT, 'plain')
    message_content_html = MIMEText(MESSAGE_HTML, 'html')

    message.attach(message_content_plain)
    message.attach(message_content_html)

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as mail_server:
        mail_server.login(SENDER, PASSWORD)
        mail_server.sendmail(SENDER, RECIPIENT, message.as_string())


def send_html_email_with_attachment():
    message = MIMEMultipart()
    message['Subject'] = SUBJECT
    message['From'] = SENDER
    message['To'] = ','.join(RECIPIENT)

    message_content_plain = MIMEText(MESSAGE_TEXT, 'plain')
    message_content_html = MIMEText(MESSAGE_HTML, 'html')

    message.attach(message_content_plain)
    message.attach(message_content_html)

    with open(ATTACHMENT, 'rb') as attachment:
        message_attachment = MIMEApplication(attachment.read())

    message_attachment.add_header(
        'Content-Disposition',
        f'attachment; filename={ATTACHMENT}',
    )

    message.attach(message_attachment)

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as mail_server:
        mail_server.login(SENDER, PASSWORD)
        mail_server.sendmail(SENDER, RECIPIENT, message.as_string())


if __name__ == '__main__':
    # send_text_email()
    # send_html_email()
    send_html_email_with_attachment()

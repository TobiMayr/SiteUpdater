import time
import smtplib
import ssl
import requests
from email.mime.text import MIMEText
from PySide2.QtCore import QRunnable
from email.mime.multipart import MIMEMultipart


class Worker(QRunnable):

    def __init__(self, status_label, source_code, keywords_dict, url):
        super().__init__()
        self.status_label = status_label
        self.source_code = source_code
        self.keywords_dict = keywords_dict
        self.url = url

    def run(self):
        tries = 0
        has_changed = False
        while not has_changed:
            time.sleep(60)
            tries = tries + 1
            self.status_label.setText(f'Versuch Nr: {tries}')
            try:
                request = requests.get(url=self.url)
            except Exception:
                self.status_label.setText('Verbindungsprobleme, skippidipapap')
                continue
            new_source_code = request.text.lower()
            for keyword, count in self.keywords_dict.items():
                new_count = new_source_code.count(keyword)
                if new_count != count:
                    has_changed = True
                    self.status_label.setText('Änderung entdeckt!!!')
                    self.send_mail(keyword)

    def send_mail(self, keyword):
        keywords = ' '.join([*self.keywords_dict])
        sender_email = 'restockbotdeluxe@gmail.com'
        password = ''
        receiver_email = 'tobistian@gmail.com'
        receiver_email2 = 'marian.mayr@hotmail.de'

        message = MIMEMultipart("alternative")
        message["Subject"] = 'Keywords: ' + keywords
        message["From"] = sender_email
        message["To"] = receiver_email2

        # Create the plain-text and HTML version of your message
        text = f"""\
        That's right bitch!
        Kauf den scheiss!
        Keywords: {keywords}
        URL: {self.url}"""
        html = f"""\
        <html>
          <body>
            <h3>That's right bitch!</h3>
            <p>
               Kauf den scheiss!<br>
               Keywords: {keywords}<br>
               URL: {self.url}<br>
               Trigger word: {keyword}
            </p>
          </body>
        </html>
        """

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email2, message.as_string()
            )
        self.status_label.setText('Mail gesendet!!!')

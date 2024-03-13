import time
from queue import Queue
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config

class MailSender:
    def __init__(self):
        self.queue = Queue()
        self.thread = threading.Thread(target=self.send)
        self.server = None
        self.SMTP_SERVER = Config.SMTP_SERVER
        self.SMTP_PORT = Config.SMTP_PORT
        self.email = Config.EMAIL
        self.password = Config.EMAIL_PASSWORD
        self.retries = Config.EMAIL_RETRIES

    def send(self):
      while True:

        if self.queue.empty():
            break

        message = self.queue.get()

        for _ in range(self.retries):
            try:
                if not self.server:
                    self.connect_to_smtp_server()

                self.server.send_message(message)

                print(f"Email sent to {message['To']}")

                break
            except Exception as e:
                print(f"An error occurred while sending the email: {str(e)}")
                time.sleep(1)

        self.queue.task_done()

    def connect_to_smtp_server(self):
        self.server = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
        self.server.starttls()
        self.server.login(self.email, self.password)

    def send_mail(self, to, subject, body, is_html=False):
        message = MIMEMultipart()
        message['From'] = self.email
        message['To'] = to
        message['Subject'] = subject
        message.attach(MIMEText(body, 'html' if is_html else 'plain'))
        self.queue.put(message)

        if not self.thread.is_alive():
            self.start()


    def start(self):
        self.thread = threading.Thread(target=self.send)
        self.thread.start()


    def check_queue(self):
        return self.queue.qsize()
    

    def __del__(self):
        if self.server:
            self.server.quit()


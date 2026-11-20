#  Imagine a notification system 

class Email:

    def send(self):
        print("Email Sent")

class SMS:

    def send(self):
        print("SMS Sent")

class Whatsapp:

    def send(self):
        print("Whatsapp Message Send")

notifications = [Email(),SMS(),Whatsapp()]

for notification in notifications:
    notification.send()
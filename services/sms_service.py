import os
from twilio.rest import Client

def send_sms(phone, message):
    client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_TOKEN"))
    client.messages.create(
        to=phone,
        from_="8668047181",
        body=message
    )
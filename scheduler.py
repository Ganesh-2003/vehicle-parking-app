from flask_apscheduler import APScheduler
from datetime import datetime
import sqlite3
import requests
from services.email_service import send_email
from services.sms_service import send_sms
from services.chat_service import send_chat
from config import DATABASE_PARKING

scheduler = APScheduler()

def send_daily_reminder():
    print("Running reminder job:", datetime.now())

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    #Need to Ensure that users with 
    #parking_created = 0 are sent reminder
    cur.execute('''
                select user_id, email, phone_no from users  
                ''')

    users = cur.fetchall()
    print(users)
    for user_id, email, phone in users:
        message = "Reminder: Please book your parking slot today!"

        #if email:
            #send_email(email, message)
        #if phone:
            #send_sms(phone, message)

        send_chat(message)

    connection.close()

def init_scheduler(app):
    scheduler.init_app(app)
    scheduler.start()

    scheduler.add_job(
    id='daily_test',
    func=send_daily_reminder,
    trigger='interval',
    hours=18,
    minute = 0
)


                                        
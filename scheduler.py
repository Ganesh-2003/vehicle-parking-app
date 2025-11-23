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


#Function for sending monthly reports 

def send_monthly_report():
    print("Running monthly report job:", datetime.now())

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    # Fetch all users
    cur.execute("SELECT user_id, name, email FROM users")
    users = cur.fetchall()

    for user_id, name, email in users:

        # Get booking data for month
        cur.execute("""
                    SELECT lot_id, parking_timestamp, parking_cost
                    FROM Reserve_Parking_Spot
                    WHERE user_id = ?
                    AND strftime('%m', parking_timestamp) = strftime('%m', 'now')
                    AND strftime('%Y', parking_timestamp) = strftime('%Y', 'now')
                """, (user_id,))
        
        bookings = cur.fetchall()

        # Build HTML report
        html = "<h2>Monthly Parking Report</h2>"
        html += f"<p>Hello {name}, here is your monthly activity summary:</p>"
        html += f"<p>Total Bookings: {len(bookings)}</p>"
        html += "<ul>"
        for b in bookings:
            html += f"<li>{b[1]} | Lot ID: {b[0]} | ₹{b[2]}</li>"
        html += "</ul>"

        # Send Email
        send_email(email, html)

    connection.close()

def init_scheduler(app):
    scheduler.init_app(app)
    scheduler.start()

    scheduler.add_job(
    id='daily_test',
    func=send_daily_reminder,
    trigger='interval',
    hours=18
    )

    # Monthly report job
    scheduler.add_job(
        id='monthly_report',
        func=send_monthly_report,
        trigger='interval',
        # day=1,
        # hour=8,
        # minute=0
        seconds = 60
    )


                                        
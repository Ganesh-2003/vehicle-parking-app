from flask import Flask
from controllers.auth_controller import auth
from controllers.admin_controller import admin
from controllers.user_controller import user
from models.parking_lot import createParkingLot, createParkingSpots,createReserveParkingSpot, createVehiclesTable
from flask_apscheduler import APScheduler
from scheduler import init_scheduler, send_daily_reminder
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__) 
app.secret_key = os.getenv("SECRET_KEY")

init_scheduler(app)
 
# @app.route("/run-reminder-now")
# def run_now():
#     send_daily_reminder()
#     return "Reminder job executed manually!"

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(user)

if __name__ == '__main__':
    createParkingLot()
    createParkingSpots()
    createReserveParkingSpot()
    createVehiclesTable()
    app.run(debug=True)
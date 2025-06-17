from flask import Flask
from controllers.auth_controller import auth
from controllers.admin_controller import admin
from controllers.user_controller import user
from models.parking_lot import createParkingLot, createParkingSpots,createReserveParkingSpot
from dotenv import load_dotenv
import os

app = Flask(__name__) 
app.secret_key = os.getenv("SECRET_KEY")

 
# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(user)

if __name__ == '__main__':
    createParkingLot()
    createParkingSpots()
    createReserveParkingSpot()
    app.run(debug=True)
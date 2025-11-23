from flask import Flask, session, jsonify
from flask_cors import CORS
from controllers.auth_controller import auth
from controllers.admin_controller import admin
from controllers.user_controller import user
from models.parking_lot import createParkingLot, createParkingSpots, createReserveParkingSpot, createVehiclesTable
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import os
import uuid

# Load env vars
load_dotenv()

# ---------------------------
# Create Flask App
# ---------------------------
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = os.getenv("SECRET_KEY")

# ---------------------------
# Register Blueprints
# ---------------------------
app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(user)

# ---------------------------
# Initialize DB Tables
# ---------------------------
createParkingLot()
createParkingSpots()
createReserveParkingSpot()
createVehiclesTable()

# ---------------------------
# Initialize APScheduler
# ---------------------------
scheduler = BackgroundScheduler()
scheduler.start()

# Import the job function AFTER scheduler starts
from scheduler.jobs import generate_csv_job


# ---------------------------
# Route: User Trigger Export
# ---------------------------
@app.route("/export-parking-history", methods=["POST"])
def export_parking_history():
    user_id = session.get("user_id")
    job_id = str(uuid.uuid4())

    scheduler.add_job(
        func=generate_csv_job,
        args=[user_id, job_id],
        id=job_id,
        replace_existing=True
    )

    return jsonify({"message": "Export started", "job_id": job_id})


# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)

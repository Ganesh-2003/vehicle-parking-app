from flask import Blueprint, render_template, request, redirect, url_for, flash, session,jsonify
from models.users import create_user_table, register_user, check_user, fetch_user
from models.parking_lot import insertVehicleDetails, checkVehicleExists
import bcrypt


user = Blueprint('user',__name__)

@user.route("/user/dashboard",methods = ['GET','POST'])
def dashboard():
    return render_template("dashboard/user_dashboard.html")

@user.route("/user/addVehicle", methods = ['GET', 'POST'])
def addVehicle():

    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get("user_id")
        vehicle_number = data.get("vehicle_number")

        if not user_id or not vehicle_number:
            return jsonify({"status": "error", "message": "Please enter all the details"})
        
        if (checkVehicleExists(vehicle_number)):
            return jsonify({"status": "error", "message": "Vehicle Number Already Exists"})
        
        insertVehicleDetails(user_id, vehicle_number)
        return jsonify({"status": "success", "message": "Vehicle added successfully!"})

    #GET Request
    user_id = session['user']
    return render_template("user/add_vehicle.html", user_id = user_id)
    
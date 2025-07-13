from flask import Blueprint, render_template, request, redirect, url_for, flash, session,jsonify
from models.users import create_user_table, register_user, check_user, fetch_user
from models.parking_lot import insertVehicleDetails, checkVehicleExists,get_availability_data, fetchOneParkingSpot, fetchVehicleUsers
import bcrypt


user = Blueprint('user',__name__)

@user.route("/user/dashboard",methods = ['GET','POST'])
def dashboard():

    availability_data = get_availability_data()
    print(availability_data)
    return render_template("dashboard/user_dashboard.html",availability_data=availability_data)

@user.route("/user/bookSpot", methods = ['GET','POST'])
def bookSpot():

    #POST METHOD 
    if request.method == "POST":

        lot_id = request.form.get('lot_id')
        location_name = request.form.get('locationName')
        spot_id = fetchOneParkingSpot(lot_id)
        user_id = session['user_id']
        vehicles_user = fetchVehicleUsers(user_id)

        #used for processing vehicles list
        print(vehicles_user)
        vehicles_list = []
        for vehicle in vehicles_user:
            print(vehicle)
            vehicles_list.append(vehicle[0])
        
        print(vehicles_list)

        if not vehicles_user:
            flash("You have no vehicles registered. Please add a vehicle before booking a spot.", "warning")
            return redirect(url_for('user.addVehicle'))
        
        return render_template("user/book_Spot.html", 
                               lot_id=lot_id, 
                               spot_id=spot_id, 
                               user_id=user_id, 
                               location_name = location_name, 
                               vehicles_user = vehicles_list
                            )


@user.route("/user/addVehicle", methods = ['GET', 'POST'])
def addVehicle():

    if request.method == 'POST':
        data = request.get_json()
        user_id = session['user_id']
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
    
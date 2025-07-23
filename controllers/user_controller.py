from flask import Blueprint, render_template, request, redirect, url_for, flash, session,jsonify
from models.users import create_user_table, register_user, check_user, fetch_user
from models.parking_lot import insertVehicleDetails, checkVehicleExists,get_availability_data, fetchOneParkingSpot, fetchVehicleUsers, insertReserveParkingSpot, updateParkingSpotStatus, getReserveParkingSpotData,getPriceParkingLot, updateVehicleStatus, deleteReserveParkingSpot
import bcrypt
import datetime

user = Blueprint('user',__name__)

@user.route("/user/dashboard",methods = ['GET','POST'])
def dashboard():

    user_id = session['user_id']
    user_parking_data = getReserveParkingSpotData(user_id)
  
    availability_data = get_availability_data()

    print(user_parking_data)
    print(availability_data)
    
    return render_template("dashboard/user_dashboard.html",availability_data=availability_data, user_parking_data = user_parking_data)

@user.route("/user/bookSpot", methods = ['GET','POST'])
def bookSpot():

    #POST METHOD 
    if request.method == "POST":

        lot_id = request.form.get('lot_id')
        location_name = request.form.get('locationName')
        spot_id = fetchOneParkingSpot(lot_id)
        user_id = session['user_id']
        vehicles_user = fetchVehicleUsers(user_id, 'F')

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
        
        insertVehicleDetails(user_id, vehicle_number,'F')
        return jsonify({"status": "success", "message": "Vehicle added successfully!"})

    #GET Request
    user_id = session['user']
    return render_template("user/add_vehicle.html", user_id = user_id)

@user.route('/user/confirmBooking', methods = ['GET','POST'])
def confirmBooking():

    if request.method == 'POST':
        data  = request.get_json()
        locationName = data.get('locationName')
        user_id = data.get('user_id')
        lot_id = data.get('lot_id')
        spot_id = data.get('spot_id')
        vehicle_number = data.get('vehicle_number')
        status = 'O'
        user_id = session['user_id']

        if not locationName or not user_id or not lot_id or not spot_id or not vehicle_number:
            flash("Something went wrong","error")
            return redirect(url_for('user.dashboard'))

        else:
            deleteReserveParkingSpot(user_id, vehicle_number)
            insertReserveParkingSpot(spot_id, lot_id, user_id, vehicle_number)
            updateParkingSpotStatus(spot_id,lot_id,status)
            updateVehicleStatus(user_id, vehicle_number, 'P')
        
        return jsonify({
            "status": "success",
            "message": "Booking Successfull"
        }),200

@user.route("/user/ReleaseSpot" , methods=['GET','POST'])
def ReleaseSpot():

    if request.method == 'POST':
        spot_id = request.form.get('spot_id')
        vehicle_number = request.form.get('vehicle_number')
        lot_id = request.form.get('lot_id')
        parking_time = request.form.get('parking_time')
        release_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        price = getPriceParkingLot(lot_id)
        

        if not spot_id or not vehicle_number or not lot_id or not parking_time or not price:
            flash("Something went wrong","error")
            return redirect(url_for('user.dashboard'))
        
        # Convert parking_time and release_time strings to datetime objects
        parking_dt = datetime.datetime.strptime(parking_time, "%Y-%m-%d %H:%M")
        release_dt = datetime.datetime.strptime(release_time, "%Y-%m-%d %H:%M")
        hour_difference = (release_dt - parking_dt).total_seconds() // 3600  # Only hour difference

        print(hour_difference )
        total_cost = price + hour_difference * price


        return render_template("user/release_spot.html", 
                              spot_id=spot_id, 
                              vehicle_number=vehicle_number, 
                              lot_id=lot_id, 
                              parking_time=parking_time, 
                              release_time=release_time, 
                              total_cost=total_cost)

@user.route("/user/confirmSpotRelease", methods = ['GET','POST'])  
def confirmSpotRelease():

    if request.method == 'POST':
        spot_id = request.form.get("spot_id")
        lot_id = request.form.get("lot_id")
        user_id = session['user_id']
        vehicle_number = request.form.get("vehicle_number")


        if not lot_id and not spot_id:
            flash("Something went wrong","error")
            return redirect(url_for('user.dashboard'))

        updateParkingSpotStatus(spot_id, lot_id, 'A')
        updateVehicleStatus(user_id, vehicle_number,'F')

        return redirect(url_for('user.dashboard'))




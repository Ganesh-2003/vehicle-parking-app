from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.users import create_user_table, register_user, check_user, fetch_user, insertVehicleDetails
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

        if user_id is None or vehicle_number is None:
            flash("Please enter all the details", "error")
            return redirect(url_for('user.addVehicle'))
        else:
            insertVehicleDetails(user_id, vehicle_number)

    user_id = session['user']
    return render_template("user/add_vehicle.html", user_id = user_id)
    
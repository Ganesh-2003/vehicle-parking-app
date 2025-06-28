from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.users import create_user_table, register_user, check_user, fetch_user
import bcrypt


user = Blueprint('user',__name__)

@user.route("/user/dashboard",methods = ['GET','POST'])
def dashboard():
    return render_template("dashboard/user_dashboard.html")

@user.route("/user/addVehicle", methods = ['GET', 'POST'])
def addVehicle():

    return render_template("user/add_vehicle.html")
    
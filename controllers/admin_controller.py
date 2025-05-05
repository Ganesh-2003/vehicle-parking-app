from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import bcrypt


admin = Blueprint('admin',__name__)

@admin.route("/admin/dashboard", methods = ['GET','POST'])
def dashboard():
    return render_template("dashboard/admin_dashboard.html")

@admin.route('/admin/addlot', methods = ['GET','POST'])
def addlot():
    
    if request.methods == 'POST':
        data = request.get_json()
        locationName = data.get('locationName')
        address = data.get('address')
        pincode = data.get('pincode')
        pricePerHour = data.get('pricePerHour')
        maxSpots = data.get('maxSpots')



    return render_template('admin/addlot.html')
    

from flask import Blueprint, render_template, request, redirect, url_for, flash, session,jsonify
from models.parking_lot import createParkingLot,insertParkingLot
import bcrypt


admin = Blueprint('admin',__name__)

@admin.route("/admin/dashboard", methods = ['GET','POST'])
def dashboard():
    return render_template("dashboard/admin_dashboard.html")

@admin.route('/admin/addlot', methods = ['GET','POST'])
def addlot():
    
    if request.method == 'POST':
        data = request.get_json()
        locationName = data.get('locationName')
        address = data.get('address')
        pincode = data.get('pincode')
        pricePerHour = data.get('pricePerHour')
        maxSpots = data.get('maxSpots')

        if not locationName or not address or not pincode or not pricePerHour or not maxSpots:
            return jsonify({
                "status": "error",
                "msg": "Please enter all the details"
            }), 400
        
        else:
            insertParkingLot(locationName,address,pincode,pricePerHour,maxSpots)
            res =  jsonify({
                "status": "success",
                "msg": "Parking lot added successfully",
                "data": {
                "locationName": locationName,
                "address": address,
                "pincode": pincode,
                "pricePerHour": pricePerHour,
                "maxSpots": maxSpots
                }
            }), 200

            
    
    createParkingLot()
    
        
    return render_template('admin/addlot.html')
    

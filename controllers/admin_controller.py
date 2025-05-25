from flask import Blueprint, render_template, request, redirect, url_for, flash, session,jsonify
from models.parking_lot import insertParkingLot,createParkingSpots, insertParkingSpots



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
            flash("Please enter all the details", "error")
            return redirect(url_for('admin.addlot'))
        
        else:
            lot_id = insertParkingLot(locationName,address,pincode,pricePerHour,maxSpots)
            maxSpots = int(maxSpots)
            # return jsonify({
            #     "status": "success",
            #     "msg": "Parking lot added successfully",
            #     "data": {
            #     "locationName": locationName,
            #     "address": address,
            #     "pincode": pincode,
            #     "pricePerHour": pricePerHour,
            #     "maxSpots": maxSpots
            #     }
            # }), 200
            createParkingSpots()
            for i in range(1,maxSpots+1):
                insertParkingSpots(lot_id, i)

            return jsonify({"status": "success", "message": "Parking Lot added successfully"}), 200
            
    return render_template('admin/addlot.html')
    

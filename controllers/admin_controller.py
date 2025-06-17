from flask import Blueprint, render_template, request, redirect, url_for, flash, session,jsonify
from models.parking_lot import insertParkingLot,createParkingSpots, insertParkingSpots, get_all_parking_lots, get_all_parking_spots, fetch_parking_lot, updateParkinglot, deleteParkingLotAndSpot, deleteParticularParkingSpot, getUsersData

admin = Blueprint('admin',__name__)

@admin.route("/admin/dashboard", methods = ['GET','POST'])
def dashboard():

    #Querying and filling parking lots in home page
    def getOccupiedValue(spots):
        occupied = 0
        for s in spots:
            if s[2] == 'O': #Getting status
                occupied = occupied+1 

        return occupied
    
    lots = get_all_parking_lots()
    print(lots)

    all_parking_lots = []
    
    for lot in lots:
        # Assuming lot is a tuple and the first element is the id
        lot_id = lot[0]
        spots = get_all_parking_spots(lot_id)
        total = len(spots)   
        occupied = getOccupiedValue(spots)
        available = total - occupied

        all_parking_lots.append({
            "lot": lot,
            "spots": spots,
            "total": total,
            "occupied": occupied,
            "available": available
        })

    print(all_parking_lots)

    return render_template("dashboard/admin_dashboard.html", lots_data = all_parking_lots)

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
            for i in range(1,maxSpots+1):
                insertParkingSpots(lot_id, i)

            return jsonify({"status": "success", "message": "Parking Lot added successfully"}), 200
            
    return render_template('admin/addlot.html')

@admin.route('/admin/edit', methods=['GET', 'POST'])
def editSpot():
    
    if request.method == 'POST':
        data = request.get_json()
        locationName = data.get('locationName')
        address = data.get('address')
        pincode = data.get('pincode')
        pricePerHour = data.get('pricePerHour')
        maxSpots = data.get('maxSpots')
        lot_id = int(data.get('lot_id'))
        print(data)

        if not locationName or not address or not pincode or not pricePerHour or not maxSpots:
            return jsonify({"status": "error", "message": "Please enter all the details"}), 400
        else:
            updateParkinglot(locationName, address, pincode, pricePerHour, maxSpots,lot_id)
            return jsonify({"status": "success", "message": "Parking lot updated successfully"}), 200
            
    lot_id = request.args.get('lot_id', type=int)
    print("Lot id : ", lot_id)
    parkinglotdata = fetch_parking_lot(lot_id)
    return render_template("admin/editParkinglot.html", parking_lot_data = parkinglotdata, lot_id = lot_id)


@admin.route('/admin/delete', methods=['GET', 'POST'])
def deletelot():
    
    lot_id = request.args.get('lot_id', type=int)

    if not lot_id:
        flash("Invalid or missing parking lot ID.", "error")
        return redirect(url_for('admin.dashboard'))

    parkinglotdata = fetch_parking_lot(lot_id)
    if not parkinglotdata:
        flash("Parking lot not found.", "error")
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        deleteParkingLotAndSpot(lot_id) #Parking lot deletion and Parking Spot deletion as well in POST METHOD

        flash("Parking lot deleted successfully.", "success")
        return redirect(url_for('admin.dashboard'))

    return render_template("admin/confirm_delete.html", parking_lot_data=parkinglotdata, lot_id=lot_id)

@admin.route('/admin/viewSpot', methods = ['GET','POST'])
def viewSpot():
    spot_id = request.args.get('spot_id',type = int)
    lot_id = request.args.get('lot_id',type = int)
    status = request.args.get('status',type = str)

    if spot_id is None or lot_id is None or status is None:
        flash("Invalid Lot Id or Spot_id")
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        deleteParticularParkingSpot(spot_id,lot_id)
    

    return render_template("admin/viewSpot.html", spot_id = spot_id, lot_id = lot_id, status = status)

@admin.route('/admin/users', methods = ['GET','POST'])
def viewUsers():
    
    users_data = getUsersData()

    return render_template("admin/userslist.html",users_data = users_data)

    

    

    

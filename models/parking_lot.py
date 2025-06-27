import sqlite3
from config import DATABASE_PARKING

def createParkingLot():
    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute(
        '''
            CREATE TABLE IF NOT EXISTS ParkingLot (
            lot_id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_name TEXT NOT NULL,
            address TEXT NOT NULL,
            pincode TEXT NOT NULL,
            price INTEGER NOT NULL, 
            maxSpots INTEGER NOT NULL
        )
        '''
    )

    connection.commit()
    connection.close()

def insertParkingLot(locationName,address,pincode,pricePerHour,maxSpots):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute(
        '''
            INSERT INTO ParkingLot (location_name, address, pincode, price, maxSpots) VALUES (?,?,?,?,?)
        ''',(locationName, address, pincode, pricePerHour, maxSpots)
    )

    connection.commit()
    connection.close()

    return cur.lastrowid

def createParkingSpots():

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS ParkingSpots (
        lot_id INTEGER NOT NULL,
        spot_id INTEGER,  -- Optional: to identify spot within a lot
        status TEXT CHECK(status IN ('O', 'A')) NOT NULL DEFAULT 'A',
        FOREIGN KEY (lot_id) REFERENCES ParkingLot(lot_id) ON DELETE CASCADE
        );
    '''
    )

    connection.commit()
    connection.close()

def createReserveParkingSpot():

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute(
            '''
                CREATE TABLE IF NOT EXISTS Reserve_Parking_Spot (
                spot_id INTEGER NOT NULL,
                lot_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                parking_timestamp DATETIME NOT NULL,
                leaving_timestamp DATETIME,
                parking_cost REAL,

                FOREIGN KEY (lot_id)  REFERENCES ParkingLot(lot_id)
                FOREIGN KEY (spot_id) REFERENCES ParkingSpots(spot_id),
                FOREIGN KEY (user_id) REFERENCES USERS(Id)
                );
            '''
    )

    connection.commit()
    connection.close()

def createVehiclesTable():

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute(
        '''
            CREATE TABLE IF NOT EXISTS Vehicle (
                user_id INTEGER NOT NULL,
                vehicle_number TEXT NOT NULL,
    
                FOREIGN KEY (user_id) REFERENCES Users(user_id)
            );
        '''
    )

    connection.commit()
    connection.close()

def insertParkingSpots(lot_id, i):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute(
        '''
            INSERT INTO ParkingSpots (lot_id, status, spot_id) VALUES (?,?,?) 
        ''',(lot_id, 'A', i)
    )

    connection.commit()
    connection.close()

def get_all_parking_lots():

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute(''' Select * from ParkingLot ''')
    lots = cur.fetchall()

    connection.commit()
    connection.close()
    
    return lots

def get_all_parking_spots(lot_id):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute('''
                    Select * from ParkingSpots where lot_id = (?)
                ''', (lot_id,))
    
    spots = cur.fetchall()

    connection.commit()
    connection.close()

    return spots

def fetch_parking_lot(lot_id):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute(
        '''
            Select * from ParkingLot where lot_id = (?)
        ''',(lot_id,)
    )

    parkinglotData = cur.fetchone()

    connection.commit()
    connection.close()

    return parkinglotData

def updateParkinglot(locationName,address,pincode,pricePerHour,maxSpots,lot_id):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()
    cur.execute('''
                UPDATE ParkingLot SET location_name = ?, address = ?, pincode = ?, price = ?, maxSpots = ?
                WHERE id = ?
            ''',(locationName,address,pincode,pricePerHour,maxSpots,lot_id)
            )
    print(lot_id)
    updated_rows = cur.rowcount
    print("Rows updated:", updated_rows)
    connection.commit()
    connection.close()
    return updated_rows  # Returns the number of rows updated, should be 1 if successful

def deleteParkingLotAndSpot(lot_id):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute( '''
                Delete from ParkingLot where lot_id = ?
                ''',(lot_id,))

    cur.execute('''
                    DELETE FROM ParkingSpots where lot_id = ?
                ''',(lot_id,))

    connection.commit()
    connection.close()

def deleteParticularParkingSpot(spot_id, lot_id):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute('''
                    DELETE FROM ParkingSpots where lot_id = ? AND spot_id = ?
                ''',(lot_id, spot_id))
    
    cur.execute('''
                    UPDATE ParkingLot
                    SET maxSpots = maxSpots - 1
                    WHERE lot_id = ? AND maxSpots > 0; 
                ''',(lot_id,))
    
    connection.commit()
    connection.close()

def getUsersData():

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute('''
                    SELECT * FROM USERS
                ''')
    
    users_data = cur.fetchall()
    
    connection.commit()
    connection.close()

    return users_data


    







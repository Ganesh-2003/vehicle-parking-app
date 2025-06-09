import sqlite3
from config import DATABASE_PARKING

def createParkingLot():
    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute(
        '''
            CREATE TABLE IF NOT EXISTS PARKINGLOT (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prime_location_name TEXT NOT NULL,
            address TEXT NOT NULL,
            pincode TEXT NOT NULL,
            price INTEGER NOT NULL,
            maximum_number_of_spots INTEGER NOT NULL
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
            INSERT INTO PARKINGLOT (prime_location_name, address, pincode, price, maximum_number_of_spots) VALUES (?,?,?,?,?)
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
        CREATE TABLE IF NOT EXISTS PARKINGSPOTS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lot_id INTEGER NOT NULL,
        status TEXT CHECK(status IN ('O', 'A')) NOT NULL DEFAULT 'A',
        spot_number INTEGER,  -- Optional: to identify spot within a lot
        FOREIGN KEY (lot_id) REFERENCES PARKINGLOT(id) ON DELETE CASCADE
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
            INSERT INTO PARKINGSPOTS (lot_id, status, spot_number) VALUES (?,?,?) 
        ''',(lot_id, 'A', i)
    )

    connection.commit()
    connection.close()

def get_all_parking_lots():

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute(''' Select * from PARKINGLOT ''')
    lots = cur.fetchall()

    connection.commit()
    connection.close()
    
    return lots

def get_all_parking_spots(lot_id):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute('''
                    Select * from PARKINGSPOTS where lot_id = (?)
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
            Select * from PARKINGLOT where id = (?)
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
                UPDATE PARKINGLOT SET prime_location_name = ?, address = ?, pincode = ?, price = ?, maximum_number_of_spots = ?
                WHERE id = ?
            ''',(locationName,address,pincode,pricePerHour,maxSpots,lot_id)
            )
    print(lot_id)
    updated_rows = cur.rowcount
    print("Rows updated:", updated_rows)
    connection.commit()
    connection.close()
    return updated_rows  # Returns the number of rows updated, should be 1 if successful

def deleteParkingLot(lot_id):

    connection = sqlite3.connect(DATABASE_PARKING)
    cur = connection.cursor()

    cur.execute( '''
        Delete from PARKINGLOT where id = ?
''',(lot_id,)
    )

    connection.commit()
    connection.close()








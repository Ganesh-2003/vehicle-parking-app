import sqlite3
from config import DATABASE_PARKINGLOT

def createParkingLot():
    connection = sqlite3.connect(DATABASE_PARKINGLOT)
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

    connection = sqlite3.connect(DATABASE_PARKINGLOT)
    cur = connection.cursor()

    cur.execute(
        '''
            INSERT INTO PARKINGLOT (prime_location_name, address, pincode, price, maximum_number_of_spots) VALUES (?,?,?,?,?)
        ''',(locationName, address, pincode, pricePerHour, maxSpots)
    )

    connection.commit()
    connection.close()




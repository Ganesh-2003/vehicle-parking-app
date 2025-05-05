import sqlite3
from config import DATABASE_PARKINGLOT

def createParkingLot():
    connection = sqlite3.connect(DATABASE_PARKINGLOT)
    cur = connection.cursor()

    cur.execute(
        '''
            CREATE TABLE IF NOT EXISTS PARKINGLOT (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prime_location_name TEXT NOT NULL UNIQUE,
            price TEXT NOT NULL,
            address TEXT NOT NULL,
            pincode TEXT NOT NULL,
            maximum_number_of_spots TEXT NOT NULL,
        )
        '''
    )

    connection.commit()
    connection.close()

def insertParkingLot():
    connection = sqlite3.connect(DATABASE_PARKINGLOT)
    cur = connection.cursor()

    cur.execute(
        '''
            INSERT INTO PARKINGLOT (prime_location_name,price,address,pincode,maximum_number_of_spots) VALUES (?,?,?,?,?,?)
        '''
    )




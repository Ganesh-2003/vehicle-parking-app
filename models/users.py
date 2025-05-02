import sqlite3
import os
from dotenv import load_dotenv 

def create_user_table():
    connection = sqlite3.connect("users.db")
    cur = connection.cursor()
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS USERS (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            EMAIL TEXT NOT NULL UNIQUE,
            PASSWORD TEXT NOT NULL,
            FULLNAME TEXT NOT NULL,
            ADDRESS TEXT NOT NULL,
            PINCODE TEXT NOT NULL 
        )
        '''
    )

    connection.commit()
    connection.close()

def check_user(email):

    connection = sqlite3.connect("users.db")
    cur = connection.cursor()
    res = cur.execute(
        '''
            SELECT EMAIL FROM USERS where EMAIL=?
        ''', (email)
    )

    connection.commit()
    connection.close()

    if(res):
        return True
    else:
        return False
    
def register_user(email, hashedpassword, fullname, address, pincode):

    connection = sqlite3.connect("users.db")
    cur = connection.cursor()
    res = cur.execute(
        '''
            INSERT INTO USERS (EMAIL, PASSWORD, FULLNAME, ADDRESS, PINCODE) VALUES (?,?,?,?,?)
        ''',(email, hashedpassword, fullname, address, pincode)
    )

    connection.commit()
    connection.close()
    
import sqlite3
import os
import bcrypt

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
        ''', (email,)
    )

    user = res.fetchone()
    connection.commit()
    connection.close()
    if user:
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

def fetch_user(email,password):

    connection = sqlite3.connect("users.db")
    cur = connection.cursor()
    cur.execute(
        '''
            SELECT * FROM USERS WHERE EMAIL = ?
        ''',(email,)        
    )

    user = cur.fetchone()
    if user:
        hashed_password = user[2]
        pass_correct = bcrypt.checkpw(password.encode('utf-8'), hashed_password)  # Encode the input password as well
        if pass_correct:
            return user

    return None
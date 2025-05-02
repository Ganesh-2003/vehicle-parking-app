from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.users import create_user_table, register_user, login_user, check_user
from flask_bcrypt import Bcrypt 

auth = Blueprint('auth',__name__)
bcrypt = Bcrypt(auth)

create_user_table()

@auth.route('/')
def home():
    return redirect(url_for('auth.login'))

@auth.route('/register',method = ['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    fullname = request.form['fullname']
    address = request.form['address']
    pincode = request.form['pincode']

    if(check_user(email)):
        flash('Email ID already exists. Please use a different email.', 'error')
        return redirect(url_for('auth.register'))
    
    #Password hashing

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') 

    if(email and hashed_password and fullname and address and pincode):
        register_user(email,password,fullname,address,pincode)
    else:
        flash('Please Enter all the details')



        


    


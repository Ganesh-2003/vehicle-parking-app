from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.users import create_user_table, register_user, check_user, fetch_user
import bcrypt

auth = Blueprint('auth',__name__)

create_user_table()

@auth.route('/')
def home():
    return render_template('login.html')

@auth.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        fullname = request.form['fullname']
        address = request.form['address']
        pincode = request.form['pincode']

        if check_user(email):
            flash('Email ID already exists. Please use a different email.', 'error')
            return render_template("register.html")
        
        # Password hashing
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        print(hashed_password)

        if (email and hashed_password and fullname and address and pincode):
            register_user(email, hashed_password, fullname, address, pincode)
            flash('Registration successful!', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Please enter all the details', 'error')

    return render_template("register.html")


@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = fetch_user(email,password)

        if(not user):
            flash('Please Enter Correct Credentials')
            return render_template("login.html")
        else:
            return redirect(url_for('auth.dashboard')) #Needs to changed
                    
    return render_template("login.html")

@auth.route('/dashboard',methods=['GET','POST'])
def dashboard():
    return render_template('dashboard.html')








        


    


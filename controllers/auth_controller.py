from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.users import create_user_table, register_user, check_user, fetch_user
from controllers.admin_controller import dashboard
import bcrypt

auth = Blueprint('auth',__name__)

create_user_table()

@auth.route('/')
def home():
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        fullname = request.form['fullname']
        address = request.form['address']
        pincode = request.form['pincode']

        #Checking Mail ID
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
        print(user)

        if(not user):
            flash('Please Enter Correct Credentials')
            return render_template("login.html")
        else:
            session['user'] = email
            session['role'] = user[len(user)-1]
            session['name'] = user[3]
            if session['role'] == 'admin':
                return redirect(url_for('admin.dashboard'))
                #return redirect(url_for('auth.admin_dashboard'))
            if session['role'] == 'user':
                return redirect(url_for('user.dashboard'))

                    
    return render_template("login.html")

 

# @auth.route('/admin/dashboard',methods=['GET','POST'])
# def admin_dashboard():

#     return render_template("dashboard/admin_dashboard.html")


# @auth.route('/logout', methods=['GET','POST'])
# def logout():

#     session.pop('user',None)
#     flash("You have been logged out")
#     return redirect(url_for('auth.login'))








from flask import Blueprint, render_template, request, redirect, url_for, flash, session,jsonify
from models.users import create_user_table, register_user, check_user, fetch_user
from controllers.admin_controller import dashboard
import bcrypt

auth = Blueprint('auth',__name__)

create_user_table()

@auth.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        fullname = request.form['fullname']
        address = request.form['address']
        pincode = request.form['pincode']
        phone_no = request.form['phone_no']

        #Checking Mail ID
        if check_user(email):
            flash('Email ID already exists. Please use a different email.', 'error')
            return render_template("register.html")
        
        # Password hashing
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        print(hashed_password)

        if (email and hashed_password and fullname and address and pincode, phone_no):
            register_user(email, hashed_password, fullname, address, pincode, phone_no)
            flash('Registration successful!', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Please enter all the details', 'error')

    return render_template("register.html")



@auth.route('/api/login', methods=['POST'])
def login_api():

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = fetch_user(email, password)
    print("Fetched user:", user)

    if not user:
        return jsonify({
            "success": False,
            "message": "Invalid credentials"
        }), 401

    # Set session (optional if you want login persistence)
    session['user_id'] = user[0]
    session['user'] = email
    session['role'] = user[-1]
    session['name'] = user[3]

    return jsonify({
        "success": True,
        "user_id": user[0],
        "email": email,
        "name": user[3],
        "role": user[-1]
    }), 200
 

# @auth.route('/admin/dashboard',methods=['GET','POST'])
# def admin_dashboard():

#     return render_template("dashboard/admin_dashboard.html")


# @auth.route('/logout', methods=['GET','POST'])
# def logout():

#     session.pop('user',None)
#     flash("You have been logged out")
#     return redirect(url_for('auth.login'))








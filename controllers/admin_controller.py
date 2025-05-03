from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.users import create_user_table, register_user, check_user, fetch_user
import bcrypt


admin = Blueprint('admin',__name__)

@admin.route("/admin/dashboard",methods = ['GET','POST'])
def dashboard():
    return render_template("dashboard/admin_dashboard.html")
    

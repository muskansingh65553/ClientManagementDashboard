from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from app import db, login_manager
from models import User
from utils.email import send_otp_email
from utils.helpers import generate_otp
from datetime import datetime, timedelta

bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            otp = generate_otp()
            user.otp = otp
            user.otp_valid_until = datetime.utcnow() + timedelta(minutes=5)
            db.session.commit()
            send_otp_email(user.email, otp)
            return redirect(url_for('auth.verify_otp', user_id=user.id))
        flash('Invalid email or password')
    return render_template('login.html')

@bp.route('/verify_otp/<int:user_id>', methods=['GET', 'POST'])
def verify_otp(user_id):
    user = User.query.get(user_id)
    if request.method == 'POST':
        otp = request.form.get('otp')
        if user and user.otp == otp and user.otp_valid_until > datetime.utcnow():
            login_user(user)
            user.otp = None
            user.otp_valid_until = None
            db.session.commit()
            return redirect(url_for('dashboard.index'))
        flash('Invalid or expired OTP')
    return render_template('otp.html', user_id=user_id)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('auth.register'))
        
        try:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            
            flash('Registration successful. Please log in.')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred during registration: {str(e)}')
            return redirect(url_for('auth.register'))
    
    return render_template('register.html')

# Add default user
def create_default_user():
    default_email = "kashya.me18@gmail.com"
    default_password = "Kashyap18@"
    
    if not User.query.filter_by(email=default_email).first():
        default_user = User(username="default_user", email=default_email)
        default_user.set_password(default_password)
        db.session.add(default_user)
        db.session.commit()
        print("Default user created successfully.")
    else:
        print("Default user already exists.")

# Call this function when initializing the app
create_default_user()

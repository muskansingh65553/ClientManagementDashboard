from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from app import db, login_manager
from models import User
from utils.helpers import generate_otp
from datetime import datetime, timedelta
import logging

bp = Blueprint('auth', __name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        logger.debug(f"Login attempt for email: {email}")
        
        try:
            user = User.query.filter_by(email=email).first()
            if user is None:
                logger.debug(f"User with email {email} not found")
                flash('Invalid email or password')
                return render_template('login.html')
            
            logger.debug(f"User found: {user.username}")
            
            if user.check_password(password):
                logger.debug("Password check successful")
                otp = generate_otp()
                user.otp = otp
                user.otp_valid_until = datetime.utcnow() + timedelta(minutes=5)
                db.session.commit()
                logger.debug(f"OTP generated for user: {otp}")
                # Instead of sending email, we'll print the OTP for testing purposes
                print(f"OTP for {user.email}: {otp}")
                return redirect(url_for('auth.verify_otp', user_id=user.id))
            else:
                logger.debug("Password check failed")
                flash('Invalid email or password')
        except Exception as e:
            logger.error(f"Error during login process: {str(e)}")
            flash('An error occurred during login. Please try again.')
    
    return render_template('login.html')

@bp.route('/verify_otp/<int:user_id>', methods=['GET', 'POST'])
def verify_otp(user_id):
    try:
        user = User.query.get(user_id)
        if user is None:
            logger.error(f"User with id {user_id} not found")
            flash('Invalid user')
            return redirect(url_for('auth.login'))

        if request.method == 'POST':
            otp = request.form.get('otp')
            logger.debug(f"OTP verification attempt for user: {user.username}")
            if user.otp == otp and user.otp_valid_until > datetime.utcnow():
                login_user(user)
                user.otp = None
                user.otp_valid_until = None
                db.session.commit()
                logger.debug(f"OTP verification successful for user: {user.username}")
                return redirect(url_for('dashboard.index'))
            logger.debug(f"OTP verification failed for user: {user.username}")
            flash('Invalid or expired OTP')
        return render_template('otp.html', user_id=user_id)
    except Exception as e:
        logger.error(f"Error in verify_otp: {str(e)}")
        flash('An error occurred. Please try again.')
        return redirect(url_for('auth.login'))

@bp.route('/logout')
@login_required
def logout():
    logger.debug(f"Logout attempt for user: {current_user.username}")
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        logger.debug(f"Registration attempt - Username: {username}, Email: {email}")
        
        if not username or not email or not password:
            logger.debug("Registration failed: Missing required fields")
            flash('All fields are required')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(username=username).first():
            logger.debug(f"Registration failed: Username '{username}' already exists")
            flash('Username already exists')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            logger.debug(f"Registration failed: Email '{email}' already exists")
            flash('Email already exists')
            return redirect(url_for('auth.register'))
        
        try:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            
            logger.debug(f"Registration successful for user: {username}")
            flash('Registration successful. Please log in.')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error during registration: {str(e)}")
            flash('An error occurred during registration. Please try again.')
            return redirect(url_for('auth.register'))
    
    return render_template('register.html')

def create_default_user():
    default_email = "kashya.me18@gmail.com"
    default_password = "Kashyap18@"
    
    if not User.query.filter_by(email=default_email).first():
        try:
            default_user = User(username="default_user", email=default_email)
            default_user.set_password(default_password)
            db.session.add(default_user)
            db.session.commit()
            logger.info("Default user created successfully.")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating default user: {str(e)}")
    else:
        logger.info("Default user already exists.")

create_default_user()
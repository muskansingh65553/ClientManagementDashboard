from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from werkzeug.security import generate_password_hash

bp = Blueprint('settings', __name__)

@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        
        if username and username != current_user.username:
            current_user.username = username
        
        if email and email != current_user.email:
            current_user.email = email
        
        if current_password and new_password:
            if current_user.check_password(current_password):
                current_user.set_password(new_password)
            else:
                flash('Current password is incorrect')
                return redirect(url_for('settings.settings'))
        
        db.session.commit()
        flash('Profile updated successfully')
        return redirect(url_for('settings.settings'))
    
    return render_template('settings.html')

from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func
from models import Client, Task
from app import db

bp = Blueprint('dashboard', __name__)

@bp.route('/')
@login_required
def index():
    total_clients = Client.query.filter_by(user_id=current_user.id).count()
    total_emails = Client.query.filter_by(user_id=current_user.id).filter(Client.email != None).count()
    total_phones = Client.query.filter_by(user_id=current_user.id).filter(Client.phone != None).count()
    lead_statuses = Client.query.filter_by(user_id=current_user.id).with_entities(Client.status).distinct().all()
    
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.due_date).limit(5).all()
    
    return render_template('dashboard.html', 
                           total_clients=total_clients,
                           total_emails=total_emails,
                           total_phones=total_phones,
                           lead_statuses=lead_statuses,
                           tasks=tasks)

@bp.route('/api/client_stats')
@login_required
def client_stats():
    status_counts = db.session.query(Client.status, func.count(Client.id)).filter_by(user_id=current_user.id).group_by(Client.status).all()
    status_data = {status: count for status, count in status_counts}
    
    email_counts = {
        'With Email': Client.query.filter_by(user_id=current_user.id).filter(Client.email != None).count(),
        'Without Email': Client.query.filter_by(user_id=current_user.id).filter(Client.email == None).count()
    }
    
    return jsonify({
        'status_data': status_data,
        'email_data': email_counts
    })

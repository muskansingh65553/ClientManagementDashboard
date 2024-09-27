from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Client, Task

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

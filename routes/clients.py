from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from flask_login import login_required, current_user
from app import db
from models import Client
from datetime import datetime

bp = Blueprint('clients', __name__)

@bp.route('/clients')
@login_required
def clients():
    clients = Client.query.filter_by(user_id=current_user.id).all()
    return render_template('clients.html', clients=clients)

@bp.route('/add_client', methods=['GET', 'POST'])
@login_required
def add_client():
    if request.method == 'POST':
        company_name = request.form.get('company_name')
        contact_name = request.form.get('contact_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        status = request.form.get('status')
        reminder_date = request.form.get('reminder_date')
        reminder_message = request.form.get('reminder_message')
        
        new_client = Client(company_name=company_name, contact_name=contact_name,
                            email=email, phone=phone, status=status,
                            user_id=current_user.id)
        
        if reminder_date:
            new_client.reminder_date = datetime.strptime(reminder_date, '%Y-%m-%d').date()
            new_client.reminder_message = reminder_message
        
        db.session.add(new_client)
        db.session.commit()
        
        flash('Client added successfully', 'success')
        return redirect(url_for('clients.clients'))
    
    return render_template('add_client.html')

@bp.route('/edit_client/<int:client_id>', methods=['GET', 'POST'])
@login_required
def edit_client(client_id):
    client = Client.query.get_or_404(client_id)
    if client.user_id != current_user.id:
        flash('You do not have permission to edit this client', 'error')
        return redirect(url_for('clients.clients'))
    
    if request.method == 'POST':
        client.company_name = request.form.get('company_name')
        client.contact_name = request.form.get('contact_name')
        client.email = request.form.get('email')
        client.phone = request.form.get('phone')
        client.status = request.form.get('status')
        reminder_date = request.form.get('reminder_date')
        client.reminder_message = request.form.get('reminder_message')
        
        if reminder_date:
            client.reminder_date = datetime.strptime(reminder_date, '%Y-%m-%d').date()
        else:
            client.reminder_date = None
        
        db.session.commit()
        flash('Client updated successfully', 'success')
        return redirect(url_for('clients.clients'))
    
    return render_template('edit_client.html', client=client)

@bp.route('/delete_client/<int:client_id>', methods=['POST'])
@login_required
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    if client.user_id != current_user.id:
        return jsonify({"error": "You do not have permission to delete this client"}), 403
    
    db.session.delete(client)
    db.session.commit()
    return jsonify({"success": True, "message": "Client deleted successfully"})

@bp.route('/api/clients')
@login_required
def api_clients():
    clients = Client.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': c.id,
        'company_name': c.company_name,
        'contact_name': c.contact_name,
        'email': c.email,
        'phone': c.phone,
        'status': c.status,
        'reminder_date': c.reminder_date.isoformat() if c.reminder_date else None,
        'reminder_message': c.reminder_message
    } for c in clients])

@bp.route('/set_reminder/<int:client_id>', methods=['POST'])
@login_required
def set_reminder(client_id):
    client = Client.query.get_or_404(client_id)
    if client.user_id != current_user.id:
        return jsonify({"error": "You do not have permission to set a reminder for this client"}), 403
    
    reminder_date = request.form.get('reminder_date')
    reminder_message = request.form.get('reminder_message')
    
    if reminder_date:
        client.reminder_date = datetime.strptime(reminder_date, '%Y-%m-%d').date()
        client.reminder_message = reminder_message
        client.last_reminder_sent = None
        db.session.commit()
        return jsonify({"success": True, "message": "Reminder set successfully"})
    else:
        return jsonify({"error": "Invalid reminder date"}), 400

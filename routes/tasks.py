from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app import db
from models import Task
from datetime import datetime

bp = Blueprint('tasks', __name__)

@bp.route('/tasks')
@login_required
def tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.due_date).all()
    return render_template('tasks.html', tasks=tasks)

@bp.route('/add_task', methods=['POST'])
@login_required
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    due_date_str = request.form.get('due_date')
    due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
    
    new_task = Task(title=title, description=description, status='Not Started',
                    due_date=due_date, user_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({"success": True, "message": "Task added successfully"})

@bp.route('/update_task_status/<int:task_id>', methods=['POST'])
@login_required
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return jsonify({"error": "You do not have permission to update this task"}), 403
    
    new_status = request.form.get('status')
    task.status = new_status
    db.session.commit()
    
    return jsonify({"success": True, "message": "Task status updated successfully"})

@bp.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return jsonify({"error": "You do not have permission to delete this task"}), 403
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({"success": True, "message": "Task deleted successfully"})

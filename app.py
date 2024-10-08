import os
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from sqlalchemy.orm import DeclarativeBase
from apscheduler.schedulers.background import BackgroundScheduler
from models import ActivityLog

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

def get_database_url():
    # Use hardcoded database connection details
    host = "localhost"  # DB_HOST
    port = "5432"       # DB_PORT
    user = "postgres"   # DB_USER
    password = "admin"  # DB_PASSWORD
    database = "crm"    # DB_NAME
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = get_database_url()
    app.config["SECRET_KEY"] = os.urandom(24)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @app.before_request
    def before_request():
        g.user = current_user

    @app.after_request
    def after_request(response):
        if current_user.is_authenticated:
            log_activity(f"Accessed: {request.path}")
        return response

    with app.app_context():
        from routes import auth, clients, dashboard, settings, tasks, admin
        app.register_blueprint(auth.bp)
        app.register_blueprint(clients.bp)
        app.register_blueprint(dashboard.bp)
        app.register_blueprint(settings.bp)
        app.register_blueprint(tasks.bp)
        app.register_blueprint(admin.bp)

        db.create_all()

        # Move the import here
        from reminders import check_and_send_reminders
        # Set up the scheduler
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=check_and_send_reminders, trigger="interval", hours=24)
        scheduler.start()

    return app

def log_activity(action):
    log = ActivityLog(user_id=current_user.id, action=action)
    db.session.add(log)
    db.session.commit()

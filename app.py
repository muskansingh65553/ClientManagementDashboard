import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from apscheduler.schedulers.background import BackgroundScheduler
from reminders import check_and_send_reminders

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SECRET_KEY"] = os.urandom(24)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    with app.app_context():
        from routes import auth, clients, dashboard, settings, tasks
        app.register_blueprint(auth.bp)
        app.register_blueprint(clients.bp)
        app.register_blueprint(dashboard.bp)
        app.register_blueprint(settings.bp)
        app.register_blueprint(tasks.bp)

        db.create_all()

        # Set up the scheduler
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=check_and_send_reminders, trigger="interval", hours=24)
        scheduler.start()

    return app

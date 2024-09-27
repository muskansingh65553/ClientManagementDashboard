from app import create_app
from apscheduler.schedulers.background import BackgroundScheduler
from reminders import check_and_send_reminders

app = create_app()

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_and_send_reminders, trigger="interval", hours=24)
    scheduler.start()
    
    app.run(host="0.0.0.0", port=5000)

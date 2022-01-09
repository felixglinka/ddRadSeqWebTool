from apscheduler.schedulers.background import BackgroundScheduler

from backend.service.CleanUpService import cleanUp

def start():
    scheduler = BackgroundScheduler(timezone='UTC')
    scheduler.add_job(cleanUp, 'cron', day_of_week='mon-sun', hour=10, minute=40)
    scheduler.start()

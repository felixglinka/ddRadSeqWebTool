from apscheduler.schedulers.background import BackgroundScheduler

from backend.service.CleanUpService import cleanUp

def start():
    scheduler = BackgroundScheduler(timezone='UTC')
    scheduler.add_job(cleanUp, 'interval', days=1)
    scheduler.start()

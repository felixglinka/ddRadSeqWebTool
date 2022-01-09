from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from backend.service.CleanUpService import cleanUp

def start():
    scheduler = BackgroundScheduler(timezone='UTC')

    trigger = CronTrigger(
        year="*", month="*", day="*", hour="10", minute="0", second="0"
    )

    scheduler.add_job(cleanUp, trigger=trigger)
    scheduler.start()

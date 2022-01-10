import logging
import os
import shutil
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import register_events, register_job

from django.conf import settings

# Create scheduler to run in a thread inside the application process
from backend.settings import CHUNKED_BASE_DIR

scheduler = BackgroundScheduler(timezone='UTC')
logger = logging.getLogger(__name__)

def cleanUp():

    logger.info('i miss you')

    currentTime = datetime.now()
    currentYear = currentTime.strftime('%Y')
    currentMonth = currentTime.strftime('%m')
    currentDay = currentTime.strftime('%d')

    for dir in os.listdir(CHUNKED_BASE_DIR):
        if dir != currentYear:
            try:
                shutil.rmtree(os.path.join(CHUNKED_BASE_DIR, dir))
            except Exception as e:
                logger.error(e)

    for dir in os.listdir(os.path.join(CHUNKED_BASE_DIR, currentYear)):
        if dir != currentMonth:
            try:
                shutil.rmtree(os.path.join(os.path.join(os.path.join(CHUNKED_BASE_DIR, currentYear)), dir))
            except Exception as e:
                logger.error(e)

    for dir in os.listdir(os.path.join(os.path.join(CHUNKED_BASE_DIR, currentYear), currentMonth)):
        if dir != currentDay:
            try:
                shutil.rmtree(os.path.join(os.path.join(os.path.join(CHUNKED_BASE_DIR, currentYear), currentMonth), dir))
            except Exception as e:
                logger.error(e)

def start():
    if settings.DEBUG:
      	# Hook into the apscheduler logger
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    # Adding this job here instead of to crons.
    # This will do the following:
    # - Add a scheduled job to the job store on application initialization
    # - The job will execute a model class method at midnight each day
    # - replace_existing in combination with the unique ID prevents duplicate copies of the job
    scheduler.add_job(cleanUp, trigger=CronTrigger(hour=12, minute=9), id="my_class_method",replace_existing=True)

    scheduler.start()
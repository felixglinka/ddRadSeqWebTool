import logging
import os, shutil
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

logger = logging.getLogger(__name__)

from backend.settings import CHUNKED_UPLOAD_PATH_BASE

def cleanUp():
    currentTime = datetime.now()
    currentYear = currentTime.strftime('%Y')
    currentMonth = currentTime.strftime('%m')
    currentDay = currentTime.strftime('%d')

    for dir in os.listdir(CHUNKED_UPLOAD_PATH_BASE):
        if dir != currentYear:
            try:
                os.chmod(os.path.join(CHUNKED_UPLOAD_PATH_BASE, dir), 775)
                shutil.rmtree(os.path.join(CHUNKED_UPLOAD_PATH_BASE, dir))
            except Exception as e:
                logger.error(e)

    for dir in os.listdir(os.path.join(CHUNKED_UPLOAD_PATH_BASE, currentYear)):
        if dir != currentMonth:
            try:
                os.chmod(os.path.join(os.path.join(os.path.join(CHUNKED_UPLOAD_PATH_BASE, currentYear)), dir), 775)
                shutil.rmtree(os.path.join(os.path.join(os.path.join(CHUNKED_UPLOAD_PATH_BASE, currentYear)), dir))
            except Exception as e:
                logger.error(e)

    for dir in os.listdir(os.path.join(os.path.join(CHUNKED_UPLOAD_PATH_BASE, currentYear), currentMonth)):
        if dir != currentDay:
            try:
                os.chmod(os.path.join(os.path.join(os.path.join(CHUNKED_UPLOAD_PATH_BASE, currentYear), currentMonth), dir), 775)
                shutil.rmtree(os.path.join(os.path.join(os.path.join(CHUNKED_UPLOAD_PATH_BASE, currentYear), currentMonth), dir))
            except Exception as e:
                logger.error(e)


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after our job has run.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone='UTC')
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            cleanUp,
            trigger=CronTrigger(hour=13, minute=50),  # Every 10 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
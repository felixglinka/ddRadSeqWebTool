import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)

class CleanUpService(AppConfig):
    name = 'api'

    def ready(self):
        logger.info('ho')
        from backend.service import Update
        Update.start()

from django.apps import AppConfig
from django.conf import settings

class CoreConfig(AppConfig):
    name = "api"

    def ready(self):
        from . import scheduler
        # if settings.SCHEDULER_AUTOSTART:
        # 	scheduler.start()
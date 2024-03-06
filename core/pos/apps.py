from django.apps import AppConfig


class PosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.pos'

    def ready(self):
        import core.pos.utilities.signals

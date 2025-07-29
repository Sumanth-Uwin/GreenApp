from django.apps import AppConfig

class EcoappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecoapp'

    def ready(self):
        import ecoapp.signals

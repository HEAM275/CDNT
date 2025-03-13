from django.apps import AppConfig


class AcuerdosConfig(AppConfig):
    name = 'Acuerdos'

    def ready(self):
        import Acuerdos.signals

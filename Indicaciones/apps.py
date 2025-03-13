from django.apps import AppConfig


class IndicacionesConfig(AppConfig):
    name = 'Indicaciones'

    def ready(self):
        import Indicaciones.signals

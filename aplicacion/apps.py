from django.apps import AppConfig


class AplicacionConfig(AppConfig):
    
    name = 'aplicacion'

    def ready(self):
        import aplicacion.signals  # Importa el archivo signals.py
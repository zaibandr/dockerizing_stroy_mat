from django.apps import AppConfig


class DischargeAppConfig(AppConfig):
    name = 'discharge_app'

    def ready(self):
        import discharge_app.signals
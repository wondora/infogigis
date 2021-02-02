from django.apps import AppConfig


class GshsConfig(AppConfig):
    name = 'gshs'
    def ready(self):
        import gshs.signals
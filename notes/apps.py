from django.apps import AppConfig


class NoteConfig(AppConfig):
    name = 'notes'

    def ready(self):
        from . import signals

from django.apps import AppConfig


class EventSourcingConfig(AppConfig):
    name = 'events_manager.event_sourcing'
    default_auto_field = 'django.db.models.BigAutoField'

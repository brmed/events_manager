from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from events_manager.event_sourcing.models.event_store import EventStore

from .base_model import BaseModel


class Event(BaseModel):
    event_store = models.ForeignKey(EventStore, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)
    diff = models.JSONField(blank=True, null=True)
    state = models.JSONField(blank=True, null=True)

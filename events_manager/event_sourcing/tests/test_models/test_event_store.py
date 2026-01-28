from django.test import TestCase
from model_bakery import baker

from events_manager.event_sourcing.models import EventStore


class EventStoreModelTestCase(TestCase):
    def test_instantiate(self):
        event_store = baker.make(EventStore)
        self.assertIsInstance(event_store, EventStore)

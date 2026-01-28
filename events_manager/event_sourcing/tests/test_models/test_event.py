from django.test import TestCase
from model_bakery import baker

from events_manager.event_sourcing.models import Event


class EventModelTestCase(TestCase):
    def test_instantiate(self):
        event = baker.make(Event)
        self.assertIsInstance(event, Event)

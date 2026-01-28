import mock
from django.test import TestCase
from django.utils import timezone

from events_manager.event_sourcing.domain import (Event, EventStore,
                                                  TrackedObject)


class EventStoreTestCase(TestCase):
    def setUp(self):
        self.user_domain = mock.Mock(
            id=20,
            username='sudo',
            first_name='Rodrigo',
            email='rodrigo@moobile.com.br'
        )

        self.attributes = dict(
            name='Evento de Criação',
            user=self.user_domain,
            date=timezone.now(),
        )

        self.tracked_object = TrackedObject()

        self.event = Event(**self.attributes)

        self.event_store = EventStore(
            tracked_object=self.tracked_object,
            events=[self.event]
        )

    def test_instantiate(self):
        self.assertIsInstance(self.event_store, EventStore)

    def test_event_is_instance(self):
        self.assertIsInstance(self.event_store.events[0], Event)

    def test_tracked_object_is_instance(self):
        self.assertIsInstance(self.event_store.tracked_object, TrackedObject)

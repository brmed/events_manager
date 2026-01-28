import mock
from django.contrib.auth.models import User as UserModel
from django.test import TestCase
from django.utils import timezone
from model_bakery import baker

from events_manager.event_sourcing.domain import TrackedObject
from events_manager.event_sourcing.models import Event, EventStore
from events_manager.event_sourcing.repositories import EventStoreRepository


class EventStoreRepositoryTestCase(TestCase):
    def setUp(self):
        self.user = baker.make(UserModel)

        self.event = mock.Mock(
            id=1,
            date=timezone.now(),
            user=self.user,
            diff=dict(),
            state=dict(),
        )

        self.event.name = 'Evento de Criação'

        self.event_store_model = baker.make(
            EventStore,
            tracked_object_id=10,
        )

        self.tracked_object = TrackedObject(
            object_id=10,
            module=self.event_store_model.module,
            signature=self.event_store_model.signature,
        )

        self.repository = EventStoreRepository()

    def test_instantiate(self):
        self.assertIsInstance(self.repository, EventStoreRepository)

    def test_get_event_store(self):
        event_store_domain = self.repository.get_event_store(self.tracked_object)

        self.assertEqual(event_store_domain.id, self.event_store_model.id)
        self.assertEqual(
            event_store_domain.tracked_object.object_id,
            self.event_store_model.tracked_object_id
        )
        self.assertEqual(
            event_store_domain.tracked_object.module,
            self.event_store_model.module
        )
        self.assertEqual(
            event_store_domain.tracked_object.signature,
            self.event_store_model.signature
        )

    def test_get_event_store_create_if_does_not_exist(self):
        self.tracked_object.object_id = 11

        number_of_event_stores = EventStore.stored.count()

        self.repository.get_event_store(self.tracked_object)

        self.assertEqual(EventStore.stored.count(), number_of_event_stores + 1)

    def test_save_new_event(self):
        number_of_events = self.event_store_model.events().count()

        self.repository.save_event(
            event=self.event,
            tracked_object=self.tracked_object
        )

        self.assertEqual(
            self.event_store_model.events().count(),
            number_of_events + 1
        )

    def test_get_event_store_return_events(self):
        self.repository.save_event(
            event=self.event,
            tracked_object=self.tracked_object
        )

        event_store_domain = self.repository.get_event_store(self.tracked_object)

        self.assertEqual(
            Event.stored.all()[0].name,
            event_store_domain.events[0].name,
        )
        self.assertEqual(
            Event.stored.all()[0].date,
            event_store_domain.events[0].date,
        )
        self.assertEqual(
            Event.stored.all()[0].user_id,
            event_store_domain.events[0].user.id,
        )
        self.assertEqual(
            Event.stored.all()[0].diff,
            event_store_domain.events[0].diff,
        )
        self.assertEqual(
            Event.stored.all()[0].state,
            event_store_domain.events[0].state,
        )

    def test_get_last_event(self):
        self.repository.save_event(
            event=self.event,
            tracked_object=self.tracked_object
        )

        last_event = self.repository.get_last_event(self.tracked_object)

        self.assertEqual(
            self.event_store_model.event_set.all()[0].name,
            last_event.name,
        )

        self.assertEqual(
            self.event_store_model.event_set.all()[0].date,
            last_event.date,
        )

        self.assertEqual(
            self.event_store_model.event_set.all()[0].user_id,
            last_event.user.id,
        )

        self.assertEqual(
            self.event_store_model.event_set.all()[0].state,
            last_event.state,
        )

        self.assertEqual(
            self.event_store_model.event_set.all()[0].diff,
            last_event.diff,
        )

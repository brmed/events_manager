import mock
from django.contrib.auth.models import User as UserModel
from django.test import TestCase
from django.utils import timezone
from model_bakery import baker

from events_manager.event_sourcing.domain import Event as EventDomain
from events_manager.event_sourcing.domain import EventStore as EventStoreDomain
from events_manager.event_sourcing.domain import TrackedObject
from events_manager.event_sourcing.factories import EventStoreFactory
from events_manager.event_sourcing.models import Event as EventModel
from events_manager.event_sourcing.models import EventStore as EventStoreModel


class EventStoreFactoryTestCase(TestCase):
    def setUp(self):
        self.user = baker.make(UserModel)

        self.user_domain = mock.Mock(
            id=20,
            username='sudo',
            first_name='Rodrigo',
            email='rodrigo@moobile.com.br'
        )

        self.event_store_model = baker.make(
            EventStoreModel,
        )

        self.event_model = baker.make(
            EventModel,
            name='Evento de Criação',
            user=self.user,
            event_store=self.event_store_model,
            diff=None,
            state={
                'nome': 'Rodrigo Bello',
                'email': 'rodrigo@moobile.com.br',
                'idade': '25',
            }
        )

        self.factory = EventStoreFactory()

        self.event_store_domain = self.factory.build_from_model(
            self.event_store_model
        )

    def test_instantiate(self):
        self.assertIsInstance(self.factory, EventStoreFactory)

    def test_build_event_from_model(self):
        event_domain = self.factory.build_event_from_model(self.event_model)

        self.assertEqual(
            event_domain.name,
            self.event_model.name,
        )

        self.assertEqual(
            event_domain.date,
            self.event_model.date,
        )

        self.assertEqual(
            event_domain.user.id,
            self.user.id,
        )

        self.assertEqual(
            event_domain.diff,
            self.event_model.diff,
        )

        self.assertEqual(
            event_domain.state,
            self.event_model.state,
        )

    def test_build_event_store_from_model(self):
        event_domain = self.event_store_domain.get_last_event()
        tracked_object = self.event_store_domain.tracked_object

        self.assertIsInstance(self.event_store_domain, EventStoreDomain)
        self.assertIsInstance(event_domain, EventDomain)
        self.assertIsInstance(tracked_object, TrackedObject)

    def test_build_event_from_tracked_object(self):
        tracked_object = TrackedObject(
            object_id=20,
            module='apps.events_manager.event_sourcing.domain',
            signature='TrackedObject',
        )

        date = timezone.now()

        event_domain = self.factory.build_event_from_tracked_object(
            user=self.user_domain,
            tracked_object=tracked_object,
            name='Evento de Criação',
            date=date
        )

        self.assertEqual(
            event_domain.name, 'Evento de Criação'
        )

        self.assertEqual(
            event_domain.state,
            dict(
                object_id=20,
                module='apps.events_manager.event_sourcing.domain',
                signature='TrackedObject',
            )
        )

        self.assertEqual(
            event_domain.date,
            date
        )

        self.assertEqual(
            event_domain.user.id,
            self.user_domain.id,
        )

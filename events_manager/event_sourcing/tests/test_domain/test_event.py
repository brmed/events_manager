import mock
from django.test import TestCase
from django.utils import timezone

from events_manager.event_sourcing.domain import Event


class EventTestCase(TestCase):
    def setUp(self):
        self.state = dict(
            nome='Rodrigo Bello',
            email='rodrigo@moobile.com.br',
            idade=25,
            endereco=dict(
                rua='Avenida Padre Leonel Franca',
                numero=90,
                bairro='Gávea',
            )
        )

        self.user_domain = mock.Mock(
            id=20,
            username='sudo',
            first_name='Rodrigo',
            email='rodrigo@moobile.com.br'
        )

        self.attributes = dict(
            name='Evento de Atualização',
            user=self.user_domain,
            date=timezone.now(),
        )

        self.event = Event(state=self.state, **self.attributes)

    def test_instantiate(self):
        self.assertIsInstance(self.event, Event)

    def test_build_diff_without_previous_state(self):
        previous_event = Event(**self.attributes)

        self.event.set_diff(previous_event)

        self.assertIsNone(self.event.diff)

    def test_build_diff_with_equal_event_stores(self):
        previous_event = Event(state=self.state, **self.attributes)

        self.event.set_diff(previous_event)

        self.assertIsNone(self.event.diff)

    def test_build_diff(self):
        previous_state = dict(
            nome='Rodrigo Bello',
            email='rodrigoabbello@gmail.com',
            idade=26,
            endereco=dict(
                rua='Avenida Padre Leonel Franca',
                numero=90,
                bairro='Gávea',
            )
        )

        previous_event = Event(state=previous_state, **self.attributes)

        expected_diff = {
            'idade': {
                'old_value': 26,
                'new_value': 25,
            },
            'email': {
                'old_value': 'rodrigoabbello@gmail.com',
                'new_value': 'rodrigo@moobile.com.br',
            },
        }

        self.event.set_diff(previous_event)

        self.assertEqual(self.event.diff, expected_diff)

    def test_build_diff_with_new_fields(self):
        previous_state = dict(
            email='rodrigoabbello@gmail.com'
        )

        previous_event = Event(state=previous_state, **self.attributes)

        expected_diff = {
            'idade': {
                'old_value': None,
                'new_value': 25,
            },
            'nome': {
                'old_value': None,
                'new_value': 'Rodrigo Bello',
            },
            'endereco': {
                'old_value': None,
                'new_value': {
                    'rua': 'Avenida Padre Leonel Franca',
                    'numero': 90,
                    'bairro': 'Gávea',
                }
            },
            'email': {
                'old_value': 'rodrigoabbello@gmail.com',
                'new_value': 'rodrigo@moobile.com.br',
            },
        }

        self.event.set_diff(previous_event)

        self.assertEqual(self.event.diff, expected_diff)

    def test_build_diff_removing_fields(self):
        previous_state = dict(
            nome='Rodrigo Abreu Bello',
            email='rodrigo@moobile.com.br',
            idade=25,
            telefone='021996510300',
            cpf='15415415415',
            endereco=dict(
                rua='Avenida Padre Leonel Franca',
                numero=90,
                bairro='Gávea',
            )
        )

        previous_event = Event(state=previous_state, **self.attributes)

        expected_diff = {
            'telefone': {
                'old_value': '021996510300',
                'new_value': None,
            },
            'cpf': {
                'old_value': '15415415415',
                'new_value': None,
            },
            'nome': {
                'old_value': 'Rodrigo Abreu Bello',
                'new_value': 'Rodrigo Bello',
            },
        }

        self.event.set_diff(previous_event)

        self.assertEqual(self.event.diff, expected_diff)

    def test_build_diff_updating_subfields(self):
        previous_state = dict(
            nome='Rodrigo Bello',
            email='rodrigo@moobile.com.br',
            idade=25,
            endereco=dict(
                rua='Rua Professor Manoel Ferreira',
                numero=101,
                bairro='Gávea',
            )
        )

        previous_event = Event(state=previous_state, **self.attributes)

        expected_diff = {
            'endereco': {
                'old_value': {
                    'rua': 'Rua Professor Manoel Ferreira',
                    'numero': 101,
                    'bairro': 'Gávea',
                },
                'new_value': {
                    'rua': 'Avenida Padre Leonel Franca',
                    'numero': 90,
                    'bairro': 'Gávea',
                },
            }
        }

        self.event.set_diff(previous_event)

        self.assertEqual(self.event.diff, expected_diff)

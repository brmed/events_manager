import mock
from django.test import TestCase

from .. import Event


class EventTestCase(TestCase):

    def setUp(self):
        self.event = Event()
        self.handler = mock.Mock()

    def test_instantiate(self):
        self.assertIsInstance(self.event, Event)

    def test_notify(self):
        self.event.notify()

    def test_connect_signal(self):
        self.event.signal = mock.Mock()
        self.event.connect_signal(self.handler)
        self.event.signal.connect.assert_called_once_with(
            self.handler.run, dispatch_uid=self.handler.uid, weak=False)

    def test_event_signal_is_singleton_for_events(self):

        class MyEvent(Event):
            pass

        my_event = MyEvent()
        my_event_2 = MyEvent()

        self.assertTrue(my_event.signal is my_event_2.signal)
        self.assertFalse(my_event is my_event_2)

    def test_events_subclasses_stores_args(self):
        class MyEvent(Event):
            pass

        args = 1, 2
        kwargs = {'span': 'eggs'}

        my_event = MyEvent(*args, **kwargs)
        self.assertEqual(args, my_event.args)
        self.assertEqual(kwargs, my_event.kwargs)

    def test_different_events_has_different_signals(self):

        class MyEvent(Event):
            pass

        class MyEvent2(Event):
            pass

        my_event = MyEvent()
        my_event2 = MyEvent2()

        self.assertFalse(my_event.signal is my_event2.signal)

import logging

from django.conf import settings
from django.dispatch import Signal


class Event:

    __signals = dict()

    def __new__(cls, *args, **kwargs):
        if not cls.__signals.get(cls):
            cls.__signals[cls] = Signal()
        cls.signal = cls.__signals[cls]
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def notify(self):
        if settings.DEBUG:
            response = self.signal.send(
                sender=self.__class__, **self.kwargs)
        else:
            response = self.signal.send_robust(
                sender=self.__class__, **self.kwargs)

        for receiver, response_item in response:
            if isinstance(response_item, Exception):
                logger = logging.getLogger('events_manager')
                logger.error(f'Events manager error: {str(response_item)}', exc_info=response_item)
        return response

    def connect_signal(self, handler):
        self.signal.connect(handler.run, dispatch_uid=handler.uid, weak=False)

from unittest import TestCase

import pygame
from pygame.event import Event
from pygame.sprite import Sprite

from zkit.eventgroup import EventGroup
from zkit.eventgroup import subscribe


class TestSprite(Sprite):

    def __init__(self, *groups):
        Sprite.__init__(self, *groups)
        self.called_events = list()

    @subscribe(pygame.KEYDOWN, key=pygame.K_ESCAPE)
    def on_K_ESCAPE_down(self, event, delta):
        self.called_events.append((event, delta))

    @subscribe("some-key", who="some-value")
    def on_some_key(self, event, delta):
        self.called_events.append((event, delta))


class TestEvent:

    def __init__(self):
        self.event_key = "some-key"
        self.who = "some-value"


class EventGroupTestCase(TestCase):

    def setUp(self):
        self.s = TestSprite()
        self.g = EventGroup()
        self.g.add(self.s)

    def test_auto_subscribe_standard_events(self):
        event = Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
        delta = 0
        self.g.update([event], delta)
        self.assertIs(self.s.called_events[0][0], event)
        self.assertEqual(self.s.called_events[0][1], delta)

    def test_filters_are_applied(self):
        event = Event(pygame.KEYDOWN, key=pygame.K_SPACE)
        delta = 0
        self.g.update([event], delta)
        self.assertEqual(len(self.s.called_events), 0)

    def test_can_use_arbitrary_event_object(self):
        event = TestEvent()
        delta = 10
        self.g.update([event], delta)
        self.assertIs(self.s.called_events[0][0], event)
        self.assertEqual(self.s.called_events[0][1], delta)

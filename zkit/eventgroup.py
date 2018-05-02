from pygame.sprite import Group

from heapq import heappush
from heapq import heappop

INFINITE_UPDATE_MSG = ("Most impressive... the game has executed %s events in "
                       "a single update! most likely an infinite loop has "
                       "occured and this frame will NEVER END! MUA HA HA HA")


def subscribe(event_key, **filter_kwargs):
    def decorator(handler):
        def decorated(*args, **kwargs):
            return Subscription(handler, event_key, **filter_kwargs)
        return decorated
    return decorator


class Subscription(object):

    def __init__(self, handler, event_key, **filter_kwargs):
        self.handler = handler
        self.event_key = event_key
        self.filter_kwargs = filter_kwargs
        self.sprite = None

    def execute_handler(self, event, delta):
        self.handler(self.sprite, event, delta)


class EventGroup(Group):

    class PossibleInfiniteEventLoopError(Exception):
        pass

    MAX_SPRITE_EVENTS_PER_UPDATE = 100000

    def __init__(self, *sprites):
        super(EventGroup, self).__init__(*sprites)
        self.subscriptions = list()
        self.sprite_events = list()

    def add(self, *sprites):
        super(EventGroup, self).add(*sprites)
        for sprite in sprites:
            self.bind_subscriptions(sprite)

    def bind_subscriptions(self, sprite):
        for key in dir(sprite):
            value = getattr(sprite, key)
            if self._is_event_handler_function(key, value):
                self._bind_subscription(sprite, value)

    def _is_event_handler_function(self, key, value):
        return callable(value) and key.startswith("on_")

    def _bind_subscription(self, sprite, subscription_factory):
        subscription = subscription_factory()
        subscription.sprite = sprite
        self.subscriptions.append(subscription)

    def update(self, events, delta):
        super(EventGroup, self).update(delta)
        self._unsubscribe_removed_sprites()
        # first handle passed-in events (presumably pygame events)
        for event in events:
            self._handle_event(event, delta)

        # now handle sprite published events until they are exhausted
        # NOTE: It's possible to get into an infinite loop here
        events_handled = 0
        while self.sprite_events:
            _, event = heappop(self.sprite_events)
            self._handle_event(event, delta)
            events_handled += 1
            if events_handled > self.MAX_SPRITE_EVENTS_PER_UPDATE:
                msg = INFINITE_UPDATE_MSG % events_handled
                raise self.PossibleInfiniteEventLoopError(msg)

    def _unsubscribe_removed_sprites(self):
        remaining_valid_subscriptions = list()
        for subscription in self.subscriptions:
            if self.has(subscription.sprite):
                remaining_valid_subscriptions.append(subscription)
        self.subscriptions = remaining_valid_subscriptions

    def _get_matching_subscription(self, event):
        # Note that the event can either be a pygame event, or any type
        # that has an event_key property
        for subscription in self.subscriptions:
            if hasattr(event, "type"):
                key = event.type
            else:
                key = event.event_key

            event_key = subscription.event_key
            filters = subscription.filter_kwargs
            if event_key == key and self._filters_match(event, **filters):
                yield subscription

    def _filters_match(self, event, **filter_kwargs):
        return all(getattr(event, k) == v for k, v in filter_kwargs.items())

    def _handle_event(self, event, delta):
        for subscription in self._get_matching_subscription(event):
            subscription.execute_handler(event, delta)

    @staticmethod
    def publish(sprite, event):
        for group in sprite.groups():
            if isinstance(group, EventGroup):
                group.publish_event(event)

    def publish_event(self, event):
        """Publish a sprite event to be handled during the current update.

Sprite events are pushed into a priority heap. Event objects can set a
event_priority attribute to cause themselves to be executed in an arbitrary
order. The smaller the event_priority number, the higher priority the event
is. When events have the same event_priority they will be executed in reverse
insertion order. The default priority is assumed to be 99999

        """
        event_priority = getattr(event, "event_priority", 99999)
        heappush(self.sprite_events, (event_priority, event))

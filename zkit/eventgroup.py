from pygame.sprite import Group


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

    def __hash__(self):
        """Make instances of Subscription to be considered the same object if
they share the same handler qualified name."""
        return hash(self.handler.__qualname__)

    def __eq__(self, other):
        return self.handler.__qualname__ == other.handler.__qualname__


class EventGroup(Group):

    def __init__(self, *sprites):
        super(EventGroup, self).__init__(*sprites)
        self.subscriptions_set = set()
        self.subscriptions = list()

    def add(self, *sprites):
        super(EventGroup, self).add(*sprites)
        for sprite in sprites:
            self.bind_subscriptions(sprite)

    def update(self, events, delta):
        for event in events:
            for subscription in self._get_matching_subscription(event):
                subscription.execute_handler(event, delta)

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

    def bind_subscriptions(self, sprite):
        for key in dir(sprite):
            value = getattr(sprite, key)
            if self._is_event_handler_function(key, value):
                self._bind_subscription(sprite, value)

    def _is_event_handler_function(self, key, value):
        return callable(value) and key.startswith("on_")

    def _bind_subscription(self, sprite, subscription_factory):
        subscription = subscription_factory()
        if subscription not in self.subscriptions_set:
            subscription.sprite = sprite
            self.subscriptions_set.add(subscription)
            self.subscriptions.append(subscription)

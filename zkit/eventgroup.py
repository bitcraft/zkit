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
        self.is_bound = False
        self.sprite = None

    def __call__(self, event, delta):
        self.handler(self.sprite, event, delta)

    def __hash__(self):
        return hash(self.handler.__qualname__)

    def __eq__(self, other):
        return self.handler.__qualname__ == other.handler.__qualname__


class EventGroup(Group):

    def __init__(self, *sprites):
        super(EventGroup, self).__init__(*sprites)
        self.subscriptions_set = set()
        self.subscriptions = list()
        self._subscriptions_need_processing = True

    def add(self, *sprites):
        super(EventGroup, self).add(*sprites)

    def update(self, events, delta):
        if self._subscriptions_need_processing:
            self.bind_unbound_subscriptions()
            self._subscriptions_need_processing = False
        for event in events:
            for subscription in self.subscriptions:
                if subscription.event_key == event.type:
                    subscription(event, delta)

    def bind_unbound_subscriptions(self):
        for sprite in self:
            for key in dir(sprite):
                value = getattr(sprite, key)
                if callable(value) and key.startswith("on_"):
                    subscription = value()
                    if subscription not in self.subscriptions_set:
                        subscription.sprite = sprite
                        self.subscriptions_set.add(subscription)
                        self.subscriptions.append(subscription)

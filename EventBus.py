import asyncio
from typing import Callable
from Events.Event import Event


class EventBus():
    def __init__(self):
        self.listeners = {}

    # adds listener to a certain event
    def add_listener(self, name: str, listener: Callable):
        if not self.listeners.get(name, None):
            self.listeners[name] = {listener}
        else:
            self.listeners[name].add(listener)

    # removes listener of a certain event
    def remove_listener(self, name: str, listener: Callable):
        self.listeners[name].remove(listener)
        if len(self.listeners[name]) == 0:
            del self.listeners[name]

    # emits the event with name and data passed
    def emit(self, name: str, event: Event):
        listeners = self.listeners.get(name, [])
        for listener in listeners:
            asyncio.create_task(listener(event))
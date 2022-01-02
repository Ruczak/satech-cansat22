import asyncio

class EventBus():
    def __init__(self):
        self.listeners = {}

    def addListener(self, name, listener):
        if not self.listeners.get(name, None):
            self.listeners[name] = {listener}
        else:
            self.listeners[name].add(listener)

    def removeListener(self, name, listener):
        self.listeners[name].remove(listener)
        if len(self.listeners[name]) == 0:
            del self.listeners[name]

    def emit(self, name, event):
        listeners = self.listeners.get(name, [])
        for listener in listeners:
            asyncio.create_task(listener(event))
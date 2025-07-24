from src.logs.listener import Listener
from collections import defaultdict


class EventManager:
    listeners: defaultdict[str, list[Listener]]

    def __init__(self):
        self.listeners = defaultdict(list)

    def subscribe(self, event_type: str, listener: Listener):
        self.listeners[event_type].append(listener)

    def unsubscribe(self, event_type: str, listener):
        self.listeners[event_type] = [
            og_listener for og_listener in self.listeners if og_listener is not listener
        ] # filter out the removed listener
    
    def notify(self, event_type: str, payload):
        for listener in self.listeners[event_type]:
            listener.update(payload)

from threading import Thread
import time

class EventBus:
    def __init__(self, thread ):
        self.__serviceThread = thread
        self.__queue = []
        pass

    # adds element to the queue (at the end)
    def add(self, event):
        self.__queue.append(event)
        self.__sendToServices(event)

    # removes first element from the queue
    def remove(self, index):
        self.queue.pop(0)
    
    # private: sends an event signal to all of services
    def __sendToServices(event):
        pass
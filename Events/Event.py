import time

class Event():
    def __init__(self, name):
        self.name = name
        self.__timestamp = time.time()

    @property
    def timestamp(self):
        return self.__timestamp
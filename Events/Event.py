import time

class Event():
    def __init__(self, name: str) -> None:
        self.name = name
        self.__timestamp = time.time()

    @property
    def timestamp(self) -> float:
        return self.__timestamp
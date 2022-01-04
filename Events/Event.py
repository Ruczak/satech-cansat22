import time

class Event():
    def __init__(self, name: str) -> None:
        self.name = name
        self.__timestamp = time.time()

    # time at witch event was emitted
    @property
    def timestamp(self) -> float:
        return self.__timestamp
from .Event import Event

class SendCsvEvent(Event):
    def __init__(self, address: int, freq: int, data: list[dict]) -> None:
        super(Event, self).__init__("sendCsv")
        self.freq = freq
        self.address = address
        self.data = data
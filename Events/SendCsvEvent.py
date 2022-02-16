from .Event import Event

class SendCsvEvent(Event):
    def __init__(self, address: int, freq: int, row: dict, byteFormat: str) -> None:
        Event.__init__(self, "sendCsv")
        self.freq = freq
        self.address = address
        self.row = row
        self.byteFormat = byteFormat
from .Event import Event

class UpdateCsvEvent(Event):
    def __init__(self, path: str, data: list[dict]):
        super(UpdateCsvEvent, self).__init__('saveCsv')
        self.path = path
        self.data = data
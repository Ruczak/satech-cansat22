from .Event import Event

class UpdateHeightEvent(Event):
    def __init__(self, pressure: float):
        super(UpdateHeightEvent, self).__init__('updateHeight')
        self.pressure = pressure
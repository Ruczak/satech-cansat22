# Sensor:
# MCP9808 - Adafruit 1782 I2C high precision temperature sensor 

from ._Service import Service

class TempService(Service):
    def __init__(self, name: str) -> None:
        super(TempService, self).__init__(name)
        
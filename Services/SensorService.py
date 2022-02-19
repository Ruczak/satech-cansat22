from ._Service import Service
from smbus2 import SMBus
from bmp280 import BMP280
from Misc.MCP9808 import MCP9808


class SensorService(Service):
    def __init__(self, name: str):
        Service.__init__(self, name)
        self.__bmp280 = BMP280(i2c_dev=SMBus(1), i2c_addr=0x76)
        self.__mcp9808 = MCP9808(address=0x18, busnum=0)

    # gets pressure from BMP280 sensor (in hPa)
    def get_pressure(self) -> float:
        return float(self.__bmp280.get_pressure())

    # gets temperature from MCP9808 sensor (in °C)
    def get_temp(self) -> float:
        return float(self.__mcp9808.readTempC())

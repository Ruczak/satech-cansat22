from ._Service import Service
from smbus2 import SMBus
from bmp280 import BMP280
from Misc.MCP9808 import MCP9808
import asyncio


class SensorService(Service):
    def __init__(self, name: str):
        Service.__init__(self, name)
        self.__bmp280 = BMP280(i2c_dev=SMBus(1), i2c_addr=0x76)
        self.__mcp9808 = MCP9808(address=0x18, busnum=0)
        self.__pressure: float = 0
        self.__temp: float = 0
        self.__task: asyncio.Task = None

    # gets pressure from BMP280 sensor (in hPa)
    @property
    def pressure(self):
        return self.__pressure

    # gets temperature from MCP9808 sensor (in °C)
    @property
    def temp(self):
        return self.__temp

    def start(self):
        async def routine():
            try:
                while True:
                    timer = asyncio.sleep(1)
                    self.__pressure = float(self.__bmp280.get_pressure())
                    self.__temp = float(self.__mcp9808.readTempC())
                    await timer
            except asyncio.CancelledError:
                print("Cancelled sensor service task.")
                raise

        self.__task = asyncio.get_running_loop().create_task(routine())
        print("Started sensor service task.")

    def stop(self):
        self.__task.cancel()

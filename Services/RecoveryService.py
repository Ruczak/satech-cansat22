from ._Service import Service
import RPi.GPIO as GPIO
import asyncio
from time import time

class RecoveryService(Service):
    def __init__(self, name: str, buzzerPin: int, freq: float = 523, delay: int = 1800):
        Service.__init__(self, name)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(buzzerPin, GPIO.OUT)
        self.__buzzer = GPIO.PWM(buzzerPin, freq)
        self.__freq: float = freq
        self.__height: float = None
        self.__seaLvlPressure: float = None
        self.isBuzzing: bool = False
        self.__delay: int = delay
        self.__start: int = time()

    def buzzerStart(self):
        async def buzzing():
            while True:
                self.buzzerOn()
                await asyncio.sleep(1)
                self.buzzerOff()
                await asyncio.sleep(3)

        if not self.isBuzzing and self.__delay + self.__start < time() :
            asyncio.get_running_loop().create_task(buzzing())
            self.isBuzzing = True
            print("Started buzzing...")

    @property
    def seaLvlPressure(self) -> float:
        return self.__seaLvlPressure

    @seaLvlPressure.setter
    def seaLvlPressure(self, value: float):
        self.__seaLvlPressure = value

    def calcHeight(self, pressure):
        self.__height = 44330 * (1 - pow(pressure / self.__seaLvlPressure, 0.1903)) 
        return self.__height

    def buzzerOn(self):
        self.__buzzer.ChangeFrequency(self.__freq)
        self.__buzzer.start(10)
    
    def buzzerOff(self):
        self.__buzzer.stop()
        
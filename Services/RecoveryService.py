from ._Service import Service
import RPi.GPIO as GPIO
import asyncio
from time import time


class RecoveryService(Service):
    def __init__(self, name: str, led_pin: int, buzzer_pin: int, freq: float = 523, delay: int = 1800):
        Service.__init__(self, name)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(buzzer_pin, GPIO.OUT)
        self.__buzzer = GPIO.PWM(buzzer_pin, freq)
        self.__freq: float = freq
        self.__height: float = None
        self.__ref_pressure: float = None
        self.is_buzzing: bool = False
        self.__delay: int = delay
        self.__start: int = time()
        self.__ledPin = led_pin
        GPIO.setup(self.__ledPin, GPIO.OUT)

    def buzzer_start(self):
        async def buzzing():
            while True:
                self.buzzer_on()
                await asyncio.sleep(1)
                self.buzzer_off()
                await asyncio.sleep(3)

        if not self.is_buzzing and self.__delay + self.__start < time() :
            asyncio.get_running_loop().create_task(buzzing())
            self.is_buzzing = True
            print("Started buzzing...")

    def led_start(self):
        async def blinking():
            for _ in range(3):
                self.led_on()
                await asyncio.sleep(0.1)
                self.led_off()
                await asyncio.sleep(0.1)

            await asyncio.sleep(1)

            while True:
                self.led_on()
                await asyncio.sleep(1)
                self.led_off()
                await asyncio.sleep(1)

        print("Started blinking...")
        asyncio.get_running_loop().create_task(blinking())

    @property
    def ref_pressure(self) -> float:
        return self.__ref_pressure

    @ref_pressure.setter
    def ref_pressure(self, value: float):
        self.__ref_pressure = value

    def calc_altitude(self, pressure):
        self.__height = 44330 * (1 - pow(pressure / self.__ref_pressure, 0.1903))
        return self.__height

    def buzzer_on(self):
        self.__buzzer.ChangeFrequency(self.__freq)
        self.__buzzer.start(10)

    def buzzer_off(self):
        self.__buzzer.stop()

    def led_on(self):
        GPIO.output(self.__ledPin, GPIO.HIGH)

    def led_off(self):
        GPIO.output(self.__ledPin, GPIO.LOW)
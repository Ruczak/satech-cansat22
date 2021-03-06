from ._Service import Service
import RPi.GPIO as GPIO
import asyncio
from time import time


class RecoveryService(Service):
    def __init__(self, name: str, led_pin: int, buzzer_pin: int, freq: float = 523, delay: int = 1800):
        Service.__init__(self, name)
        self.__freq: float = freq
        self.__altitude: float = None
        self.__ref_pressure: float = None
        self.__delay: int = delay
        self.__start: float = time()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(buzzer_pin, GPIO.OUT)
        self.__buzzer = GPIO.PWM(buzzer_pin, freq)
        self.is_buzzing: bool = False

        self.__led_pin = led_pin
        GPIO.setup(self.__led_pin, GPIO.OUT)

        self.__buzzing_task: asyncio.Task = None
        self.__led_task: asyncio.Task = None

    # starts buzzing coroutine
    def buzzer_start(self):
        async def buzzing():
            try:
                while True:
                    self.buzzer_on()
                    await asyncio.sleep(1)
                    self.buzzer_off()
                    await asyncio.sleep(3)
            except asyncio.CancelledError:
                print("Stopped buzzing.")
                self.buzzer_off()
                raise

        asyncio.get_running_loop().create_task(buzzing())
        self.is_buzzing = True
        print(f"Started buzzing (altitude: {self.__altitude} m)")

    # stops buzzing coroutine
    def buzzer_stop(self):
        self.__buzzing_task.cancel()

    # starts led blinking coroutine
    def led_start(self):
        async def blinking():
            try:
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
            except asyncio.CancelledError:
                print("Stopped blinking.")
                self.led_off()
                raise

        print("Started blinking...")
        asyncio.get_running_loop().create_task(blinking())

    # stops led blinking coroutine
    def led_stop(self):
        self.__led_task.cancel()

    # gets referential pressure
    @property
    def ref_pressure(self) -> float:
        return self.__ref_pressure

    # sets referential pressure
    @ref_pressure.setter
    def ref_pressure(self, value: float):
        self.__ref_pressure = value

    # updates altitude using pressure
    async def update_altitude(self, pressure):
        try:
            self.__altitude = 44330 * (1 - pow(pressure / self.__ref_pressure, 0.1903))
            if self.__altitude < 1000 and self.__delay + self.__start < time() and not self.is_buzzing:
                self.buzzer_start()

        except asyncio.CancelledError:
            print("Cancelled updating altitude.")
            raise

    # turns buzzer on
    def buzzer_on(self):
        self.__buzzer.ChangeFrequency(self.__freq)
        self.__buzzer.start(10)

    # turns buzzer off
    def buzzer_off(self):
        self.__buzzer.stop()

    # turns led on
    def led_on(self):
        GPIO.output(self.__led_pin, GPIO.HIGH)

    # turns led off
    def led_off(self):
        GPIO.output(self.__led_pin, GPIO.LOW)

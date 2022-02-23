from gps import *
from ._Service import Service
import subprocess
import asyncio


class GPSService(Service):
    def __init__(self, name: str):
        Service.__init__(self, name)
        self.__gps = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) 
        self.__latitude: float = 0.0
        self.__longitude: float = 0.0
        self.__timestamp: str = 'n/a'
        self.__task: asyncio.Task = None

    def start(self):

        delay = asyncio.sleep(1)

        exit_code = subprocess.run("sudo stty -F /dev/ttyUSB0 9600".split(' '))
        if exit_code == 0:
            print("Set baud rate of /dev/ttyUSB0 to 9600")
        else:
            print(f"Error, could not set baud rate of /dev/ttyUSB0 to 9600 (exit_code: {exit_code})")

        await delay

        async def routine():
            try:
                while True:
                    timer = asyncio.sleep(1)
                    self.__update()
                    await timer
            except asyncio.CancelledError:
                print("Cancelled GPS Service task.")
                raise

        self.__task = asyncio.get_running_loop().create_task(routine())
        print("Started GPS service task.")

    def stop(self):
        self.__task.cancel()

    @property
    def latitude(self):
        return self.__latitude

    @property
    def longitude(self):
        return self.__longitude

    @property
    def timestamp(self):
        return self.__timestamp

    def __update(self):
        report = self.__gps.next()
        if report['class'] == 'TPV':
            self.__latitude = getattr(report,'lat', 0.0)
            self.__longitude = getattr(report,'lon', 0.0)
            self.__timestamp = getattr(report, 'time', 'n/a')
            # print(report)


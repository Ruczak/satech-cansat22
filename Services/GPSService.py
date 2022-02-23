from gps import *
from ._Service import Service
import asyncio


class GPSService(Service):
    def __init__(self, name: str):
        Service.__init__(self, name)
        self.__gps = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) 
        self.__latitude: float = 0.0
        self.__longitude: float = 0.0
        self.__timestamp: str = 'n/a'
        self.__task: asyncio.Task = None

    # starts GPS coroutine
    def start(self):
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

    # stops GPS coroutine
    def stop(self):
        self.__task.cancel()

    # gets current latitude
    @property
    def latitude(self):
        return self.__latitude

    # gets current longitude
    @property
    def longitude(self):
        return self.__longitude

    # gets last update timestamp
    @property
    def timestamp(self):
        return self.__timestamp

    # fetches GPS data from GPS device
    def __update(self):
        report = self.__gps.next()
        if report['class'] == 'TPV':
            self.__latitude = getattr(report,'lat', 0.0)
            self.__longitude = getattr(report,'lon', 0.0)
            self.__timestamp = getattr(report, 'time', 'n/a')

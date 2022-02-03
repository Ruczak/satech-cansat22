from gps import *
from ._Service import Service

class GPSService(Service):
    def __init__(self, name: str):
        Service.__init__(self, name)
        self.__gps = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) 
        self.__latitude: float = 0.0
        self.__longitude: float = 0.0
        self.__timestamp: str = 'n/a'

    @property
    def latitude(self):
        return self.__latitude

    @property
    def longitude(self):
        return self.__longitude

    @property
    def timestamp(self):
        return self.__timestamp

    def updateLoc(self):
        report = self.__gps.next()
        if report['class'] == 'TPV':
            self.__latitude = getattr(report,'lat', 0.0)
            self.__longitude = getattr(report,'lon', 0.0)
            self.__timestamp = getattr(report, 'time', 'n/a')
            # print(report)
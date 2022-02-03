from Services.FileService import FileService
from Services.CommunicationService import CommunicationService
from Services.SensorService import SensorService
from Services.SDRService import SDRService
from Services.GPSService import GPSService
from EventBus import EventBus

from Events.Event import Event
from Events.UpdateCsvEvent import UpdateCsvEvent
from Events.SendCsvEvent import SendCsvEvent

from smbus2 import SMBus
from bmp280 import BMP280

import asyncio
import time
import random

# used for debugging
def getRandomValue(min, max):
    return random.random() * max + min

def main():
    loop = asyncio.get_event_loop()
    
    eventBus = EventBus()
    fileService = FileService('File Service', './.cache')
    commService = CommunicationService('Communication Service', 20)
    sensService = SensorService('Sensor Service')
    sdrService = SDRService("SDR Service")
    gpsService = GPSService("GPS Service")

    async def updateGPS():
        while True:
            gpsService.updateLoc()
            await asyncio.sleep(1)

    async def readPressureAndTemp():
        sdrService.start("117975k", "950M", "125k", "sdr_data.csv")

        while True:
            await asyncio.sleep(1)
            data = [{'timestamp': time.time(), 'temp': sensService.getTemp(), 'pressure': sensService.getPressure(), 'lat': gpsService.latitude, 'lon': gpsService.longitude}]
            updateEvent = UpdateCsvEvent('atmData.csv', data)
            sendEvent = SendCsvEvent(22, 868, data)
            eventBus.emit('saveTempAndPressure', updateEvent)
            eventBus.emit('sendTempAndPressure', sendEvent)
        

    async def saveFileHandler(e: UpdateCsvEvent):
        fileService.addToCsv(e.path, e.data)
        print(f"Added data to csv ({e.path}, {e.data})")

    async def sendHandler(e: SendCsvEvent):
        commService.send(e.address, e.freq, e.data)
        print(f"Sent data to address of ({e.address}, {e.freq} MHz), {e.data}")
        
    eventBus.addListener('saveTempAndPressure', saveFileHandler)
    eventBus.addListener('sendTempAndPressure', sendHandler)

    try:
        gpsTask = loop.create_task(updateGPS())
        loop.run_until_complete(readPressureAndTemp())
    except KeyboardInterrupt:
        pass
    finally:
        sdrService.end()
        loop.close()
        print("Closed")


if __name__ == '__main__':
    main()

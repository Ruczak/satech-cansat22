from Services.FileService import FileService
from Services.CommunicationService import CommunicationService
from Services.SensorService import SensorService
from Services.SDRService import SDRService
from Services.GPSService import GPSService
from Services.RecoveryService import RecoveryService
from EventBus import EventBus

from Events.UpdateCsvEvent import UpdateCsvEvent
from Events.SendCsvEvent import SendCsvEvent
from Events.UpdateHeightEvent import UpdateHeightEvent

from smbus2 import SMBus
from bmp280 import BMP280

import asyncio
import time
import random
import RPi.GPIO as GPIO

def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    eventBus = EventBus()
    fileService = FileService('File Service', './.cache')
    commService = CommunicationService('Communication Service', 20)
    sensService = SensorService('Sensor Service')
    sdrService = SDRService("SDR Service")
    gpsService = GPSService("GPS Service")
    recService = RecoveryService("Recovery Service", 26, 21, delay=5)
    recService.seaLvlPressure = 1010.00

    async def updateGPS():
        while True:
            gpsService.updateLoc()
            await asyncio.sleep(1)

    async def readPressureAndTemp():
        sdrService.start("117975k", "950M", "125k", "sdr_data.csv")
        recService.ledStart()
        while True:
            await asyncio.sleep(1)
            pressure = sensService.getPressure()
            #pressure = random.randint(800, 1010)
            data = [{'timestamp': time.time(), 'temp': sensService.getTemp(), 'pressure': pressure, 'lat': gpsService.latitude, 'lon': gpsService.longitude}]
            #data = [{'timestamp': time.time(), 'temp': random.randint(-10,10), 'pressure': pressure, 'lat': 0, 'lon': 0}]
            updateEvent = UpdateCsvEvent('atmData.csv', data)
            sendEvent = SendCsvEvent(22, 868, data)
            heightEvent = UpdateHeightEvent(pressure)
            eventBus.emit('saveTempAndPressure', updateEvent)
            eventBus.emit('sendTempAndPressure', sendEvent)
            eventBus.emit('updateHeight', heightEvent)
        
    async def updateHeightHandler(e: UpdateHeightEvent):
        height = recService.calcHeight(e.pressure)
        print(f"Current height: {height}")
        if height < 500:
            recService.buzzerStart()

    async def saveFileHandler(e: UpdateCsvEvent):
        fileService.addToCsv(e.path, e.data)
        print(f"Added data to csv ({e.path}, {e.data})")

    async def sendHandler(e: SendCsvEvent):
        commService.send(e.address, e.freq, e.data)
        print(f"Sent data to address of ({e.address}, {e.freq} MHz), {e.data}")
        
    eventBus.addListener('saveTempAndPressure', saveFileHandler)
    eventBus.addListener('sendTempAndPressure', sendHandler)
    eventBus.addListener('updateHeight', updateHeightHandler)

    try:
        gpsTask = loop.create_task(updateGPS())
        loop.run_until_complete(readPressureAndTemp())
    except KeyboardInterrupt:
        pass
    finally:
        sdrService.end()
        loop.close()
        GPIO.cleanup()
        print("Closed")


if __name__ == '__main__':
    main()

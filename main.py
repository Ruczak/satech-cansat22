from Services.FileService import FileService
from Services.CommunicationService import CommunicationService
from EventBus import EventBus

from Events.UpdateCsvEvent import UpdateCsvEvent
from Events.SendCsvEvent import SendCsvEvent

import os
import asyncio
import time
import random

def getRandomValue(min, max):
    return random.random() * max + min

async def readPressureAndTemp(eventBus):
    while True:
        await asyncio.sleep(1)
        temp = getRandomValue(0, 50)
        pressure = getRandomValue(900, 1020)
        timestamp = time.time()
        updateEvent = UpdateCsvEvent('atmData.csv', [{'timestamp': time, 'temp': temp, 'pressure': pressure}])
        sendEvent = SendCsvEvent(30, 868, [{'timestamp': time, 'temp': temp, 'pressure': pressure}])
        eventBus.emit('saveTempAndPressure', updateEvent)
        eventBus.emit('sendTempAndPressure', sendEvent)

def main():
    loop = asyncio.get_event_loop()
    
    eventBus = EventBus()
    fileService = FileService('File Service', './.cache')
    commService = CommunicationService('Communication Service', 20)

    async def updateHandler(e: UpdateCsvEvent):
        fileService.addToCsv(e.path, e.data)
        print(f"Added data to csv ({e.path}, {e.data})")

    async def sendHandler(e: SendCsvEvent):
        commService.send(e.address, e.freq, e.data)
        print(f"Sent data to address of 30 (frequency: 868M), {e.data}")
        

    eventBus.addListener('saveTempAndPressure', updateHandler)
    eventBus.addListener('sendTempAndPressure', sendHandler)

    try:
        asyncio.ensure_future(readPressureAndTemp(eventBus))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Closed")
        loop.close()


if __name__ == '__main__':
    main()
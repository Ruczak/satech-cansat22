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

async def readPressureAndTemp(eventBus: EventBus):
    while True:
        await asyncio.sleep(1)
        data = [{'timestamp': time.time(), 'temp': getRandomValue(-20, 50), 'pressure': getRandomValue(900, 1020)}]
        updateEvent = UpdateCsvEvent('atmData.csv', data)
        sendEvent = SendCsvEvent(0, 868, data)
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
        print(f"Sent data to address of ({e.address}, {e.freq}M), {e.data}")
        

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
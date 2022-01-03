from Services.FileService import FileService
from EventBus import EventBus
from Events.UpdateCsvEvent import UpdateCsvEvent

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
        event = UpdateCsvEvent('atmData.csv', [{'timestamp': time.time(), 'temp': temp, 'pressure': pressure}])
        eventBus.emit('saveTempAndPressure', event)

def main():
    loop = asyncio.get_event_loop()
    
    eventBus = EventBus()
    fileService = FileService('File Service', './.cache')

    async def eventHandler(e: UpdateCsvEvent):
        fileService.addToCsv(e.path, e.data)
        print(f"Added data to csv ({e.path}, {e.data})")

    eventBus.addListener('saveTempAndPressure', eventHandler)

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
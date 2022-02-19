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

import asyncio
import time
import random
# noinspection PyUnresolvedReferences
import RPi.GPIO as GPIO


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    event_bus = EventBus()
    file_service = FileService('File Service', './.cache')
    comm_service = CommunicationService('Communication Service', 20)
    sens_service = SensorService('Sensor Service')
    sdr_service = SDRService("SDR Service")
    gps_service = GPSService("GPS Service")
    rec_service = RecoveryService("Recovery Service", 21, delay=5)
    rec_service.ref_pressure = 1010.00

    async def main_coroutine():
        sdr_service.start("800M", "1000M", "125k", "sdr_data.csv")
        gps_service.start()
        rec_service.led_start()

        rec_service.ref_pressure = sens_service.get_pressure()
        print("Sea Level Pressure set to:", rec_service.ref_pressure)

        while True:
            await asyncio.sleep(1)
            # pressure = random.randint(800, 1010)
            data = {'timestamp': time.time(), 'temp': sens_service.get_temp(), 'pressure': sens_service.get_pressure(),
                    'lat': gps_service.latitude, 'lon': gps_service.longitude}
            # data = {'timestamp': time.time(), 'temp': random.randint(-10,10), 'pressure': pressure, 'lat': 0,
            # 'lon': 0}
            update_event = UpdateCsvEvent('atm_data.csv', data)
            send_event = SendCsvEvent(22, 868, tuple(data.values()), "5d")
            altitude_event = UpdateHeightEvent(data['pressure'])
            event_bus.emit('saveTempAndPressure', update_event)
            event_bus.emit('sendTempAndPressure', send_event)
            event_bus.emit('updateAltitude', altitude_event)

    async def altitude_handler(e: UpdateHeightEvent):
        height = rec_service.calc_altitude(e.pressure)
        print(f"Current altitude: {height}")
        if height < 500:
            rec_service.buzzer_start()

    async def save_file_handler(e: UpdateCsvEvent):
        file_service.add_to_csv(e.path, e.data)
        print(f"Added data to csv ({e.path}, {e.data})")

    async def send_handler(e: SendCsvEvent):
        comm_service.send(e.address, e.freq, e.row, e.byteFormat)
        print(f"Sent data to address of ({e.address}, {e.freq} MHz), {e.row}")

    event_bus.add_listener('saveTempAndPressure', save_file_handler)
    event_bus.add_listener('sendTempAndPressure', send_handler)
    event_bus.add_listener('updateAltitude', altitude_handler)

    try:
        loop.run_until_complete(main_coroutine())
    except KeyboardInterrupt:
        pass
    finally:
        sdr_service.end()
        loop.close()
        GPIO.cleanup()
        print("Closed")


if __name__ == '__main__':
    main()

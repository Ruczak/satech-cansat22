from Services.FileService import FileService
from Services.CommunicationService import CommunicationService
from Services.SensorService import SensorService
from Services.SDRService import SDRService
from Services.GPSService import GPSService
from Services.RecoveryService import RecoveryService

import asyncio
import time
import random
# noinspection PyUnresolvedReferences
import RPi.GPIO as GPIO


async def main():
    file_service = FileService('File Service', './.cache')
    comm_service = CommunicationService('Communication Service', 20)
    sens_service = SensorService('Sensor Service')
    sdr_service = SDRService("SDR Service")
    gps_service = GPSService("GPS Service")
    rec_service = RecoveryService("Recovery Service", 26, 21, freq=1397, delay=5)
    rec_service.ref_pressure = 1010.00

    try:
        sdr_service.start("800M", "1000M", "125k", "sdr_data.csv")
        gps_service.start()
        rec_service.led_start()
        sens_service.start()

        await asyncio.sleep(1)

        rec_service.ref_pressure = sens_service.pressure
        print("Sea Level Pressure set to:", rec_service.ref_pressure)

        while True:
            timer = asyncio.sleep(1)

            data = {'timestamp': time.time(), 'temp': sens_service.temp, 'pressure': sens_service.pressure,
                    'lat': gps_service.latitude, 'lon': gps_service.longitude}
            # data = {'timestamp': time.time(), 'temp': random.randint(-10,10), 'pressure': random.randint(800,
            # 1020), 'lat': 0, 'lon': 0}

            asyncio.get_running_loop().create_task(file_service.add_to_csv('atm_data.csv', data))
            asyncio.get_running_loop().create_task(comm_service.send(22, 868, tuple(data.values()), "5d"))
            asyncio.get_running_loop().create_task(rec_service.update_altitude(data['pressure']))

            await timer
    except asyncio.CancelledError:
        sdr_service.stop()
        sens_service.stop()
        gps_service.stop()
        loop.close()
        GPIO.cleanup()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        loop.stop()
        print("Closed")

import asyncio
from Misc.sx126x import sx126x
from ._Service import Service
import struct


class CommunicationService(Service, sx126x):
    def __init__(self, name: str, address: int):
        sx126x.__init__(self, serial_num="/dev/ttyS0", freq=868, addr=address, power=22, rssi=False, air_speed=2400, relay=False)
        Service.__init__(self, name)

    # encode data to bytes using certain format
    @staticmethod
    def encode(row: tuple, byte_format: str):
        return struct.pack(byte_format, *row)

    # decode bytes to values using certain format
    @staticmethod
    def decode(data: bytes, byte_format: str):
        return struct.unpack(byte_format, data)

    # send row in specified format by frequency to address
    async def send(self, address: int, freq: int, row: tuple, byte_format: str) -> None:
        try:
            offset_frequency = int(freq) - (850 if int(freq) > 850 else 410)
            buffer = CommunicationService.encode(row, byte_format)
            data = bytes([int(address) >> 8]) + bytes([int(address) & 0xff]) + bytes([offset_frequency]) + bytes([self.addr >> 8]) + bytes([self.addr & 0xff]) + bytes([self.offset_freq]) + buffer

            sx126x.send(self, data)
            print(f"Sent data to {address} / {freq} MHz: {buffer.hex()}")
        except asyncio.CancelledError:
            print("Cancelled sending data.")
            raise

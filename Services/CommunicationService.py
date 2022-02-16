from Misc.sx126x import sx126x
from ._Service import Service
import struct

class CommunicationService(Service, sx126x):
    def __init__(self, name: str, address: int):
        sx126x.__init__(self, serial_num = "/dev/ttyS0",freq=868, addr=address, power=22, rssi=True, air_speed=2400, relay=False)
        Service.__init__(self, name)

    def encode(row: tuple, byteFormat: str):
        return struct.pack(byteFormat, *row)

    def decode(data: bytes, byteFormat: str):
        return struct.unpack(byteFormat, data)

    def send(self, address: int, freq: int, row: tuple, byteFormat: str):
        offset_frequence = int(freq) - (850 if int(freq) > 850 else 410)
        
        # the sending message format
        #
        #         receiving node              receiving node                   receiving node           own high 8bit           own low 8bit                 own 
        #         high 8bit address           low 8bit address                    frequency                address                 address                  frequency             message payload
        data = bytes([int(address)>>8]) + bytes([int(address)&0xff]) + bytes([offset_frequence]) + bytes([self.addr>>8]) + bytes([self.addr&0xff]) + bytes([self.offset_freq]) + CommunicationService.encode(row, byteFormat)

        sx126x.send(self, data)
from ._Service import Service
import typing
from rtlsdr import RtlSdr


class SDRService(Service):
    def __init__(self, name: str):
        Service.__init__(self, name)
        # self.__process = None
        self.__sdr: RtlSdr = None

    # starts SDR service
    def start(self, sample_rate: float, center_freq: float, freq_correction=60, gain: typing.Any = 'auto'):
        self.__sdr = RtlSdr()
        self.__sdr.sample_rate = sample_rate
        self.__sdr.center_freq = center_freq
        self.__sdr.freq_correction = freq_correction
        self.__sdr.gain = gain

    # reads sample from the device
    def get_samples(self, sample_count: int):
        return self.__sdr.read_samples(sample_count)

    # closes SDR service
    def close(self):
        self.__sdr.close()

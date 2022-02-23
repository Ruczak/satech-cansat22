from ._Service import Service
import subprocess
import asyncio
from rtlsdr import RtlSdr


class SDRService(Service):
    def __init__(self, name: str):
        Service.__init__(self, name)
        # self.__process = None

        self.__sdr: RtlSdr = None
        self.__task: asyncio.Task = None

    # starts SDR service
    def start(self, sample_rate: int, center_freq: int, freq_correction=60, gain='auto'):
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

    # # opens new RTL_SDR subprocess
    # def rtl_start(self, freq_min: str, freq_max: str, step: str, file: str):
    #     self.__process = subprocess.Popen(['rtl_power', '-f', f"{freq_min}:{freq_max}:{step}", file])
    #
    # # terminates RTL_SDR subprocess
    # def rtl_stop(self):
    #     self.__process.terminate()
    #     print("Stopped sdr subprocess.")


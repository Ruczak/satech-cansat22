from ._Service import Service
import subprocess


class SDRService(Service):
    def __init__(self, name: str):
        super(SDRService, self).__init__(name)
        self.__process = None

    # opens new RTL_SDR subprocess
    def start(self, freq_min: str, freq_max: str, step: str, file: str):
        self.__process = subprocess.Popen(['rtl_power', '-f', f"{freq_min}:{freq_max}:{step}", file])

    # terminates RTL_SDR subprocess
    def stop(self):
        self.__process.terminate()
        print("Stopped sdr subprocess.")


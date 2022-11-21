import pyaudio

class Mics:
    def __init__(self):
        self.deviceID = self.get_device_info()
        self.p = pyaudio.PyAudio()
        return

    def get_device_info(self):
        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')

        for i in range(0, numdevices):
            if (self.p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                if 'seeed' in self.p.get_device_info_by_host_api_device_index(0, i).get('name'):
                    return i
            else:
                print(f"Output Device id {i} - {self.p.get_device_info_by_host_api_device_index(0,i).get('name')}")


            


if __name__ == "__main__":
    m = Mics()


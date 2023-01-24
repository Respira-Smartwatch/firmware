import smbus

class GSRDriver:
    def __init__(self, f_s=256):
        self.channel = 1
        self.address = 0x8
        self.bus = smbus.SMBus(self.channel)
        self.sample_rate = f_s

        if not self._connect():
            print("NO Device Found / Connection Error")
            exit(1)


    def _connect(self):
        try:
            return self.bus.read_byte_data(self.address, 1)
        except:
            return 0
    
    def read_once(self):
        return self.bus.read_byte_data(self.address, 1)
    
    def get_sample(self):
        return [self.read_once() for _ in range(self.sample_rate)]
    
if __name__ == "__main__":
    gsr = GSRDriver()

    for i in range(10):
        print(gsr.read())
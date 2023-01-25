import smbus

class GSRDriver:
    def __init__(self, f_s=256):
        self.channel = 1
        self.address = 0x8
        self.bus = smbus.SMBus(self.channel)
        self.sample_rate = f_s
        self.error_cnt = 10

        if not self._connect():
            print("NO Device Found / Connection Error")
            exit(1)


    def _connect(self):
        try:
            return self.bus.read_byte_data(self.address, 1)
        except:
            return 0
    
    #TODO: Currently does not regulate rate : FIX THIS
    def read_once(self):
        try:
            return self.bus.read_byte_data(self.address, 1)
        except OSError:
            self.error_cnt -= 1
            return self.read_once() if self.error_cnt else -1
    
    def get_sample(self):
        return [self.read_once() for _ in range(self.sample_rate)]
    
if __name__ == "__main__":
    gsr = GSRDriver()

    for i in range(10):
        print(gsr.read_once())

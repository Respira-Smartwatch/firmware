import smbus

class GSR:
    def __init__(self):
        self.channel =1
        self.address=0x8
        self.bus = smbus.SMBus(self.channel)
        
        if not self._connect():
            print("NO DEVICE FOUND/CONNECTION ERROR")
            exit(1)

    def _connect(self):
        try:
            return self.bus.read_byte_data(self.address,1)
        except:
            return 0

    
    def read(self):
        return self.bus.read_byte_data(self.address, 1)

if __name__ == "__main__":
    gsr = GSR()
    
    for i in range(10):
        print(gsr.read())
        

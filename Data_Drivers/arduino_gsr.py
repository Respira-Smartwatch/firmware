import smbus

class GSR:
    def __init__(self):
        self.address = 0x5
        self.bus = smbus.SMBus(0)
    
    def read(self):
        return self.bus.read_byte_data(self.address,1)

if __name__ == "__main__":
    gsr = GSR()

    print(gsr.read())
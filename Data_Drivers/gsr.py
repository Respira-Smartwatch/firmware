import smbus

class GSR:
    def __init__(self):
        self.channel =1
        self.address=0x5
        self.bus = smbus.SMBus(self.channel)

    def read(self):
        return self.bus.read_byte_data(self.address)

if __name__ == "__main__":
    gsr = GSR()

    print(gsr.read())
        

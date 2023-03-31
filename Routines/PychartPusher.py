import serial


# Pychart Pusher
# This class creates a serial bus, collects a message,
# and sends that message on command.
# you can send a message directly, or add to a growing message
# that can be sent all at once at a later time
class PychartPusher:
    def __init__(self, bus: str = "/dev/ttyS0", baud: int = 115200):
        self.bus_name = bus
        self.baud = baud

        try:
            self.bus = serial.Serial(self.bus_name,
                                     baudrate=self.baud,
                                     parity=serial.PARITY_NONE,
                                     stopbits=serial.STOPBITS_ONE,
                                     bytesize=serial.EIGHTBITS,
                                     timeout=1)
        except serial.SerialException:
            print(f"Serial Error - Could not connect to {self.bus_name}")
            exit(1)

        self.message = ""

    def push(self, val: str):
        self.message += val
        return self.message

    def pop(self, num: int):
        if num < len(self.message):
            self.message = self.message[:-num]
            return self.message
        print(f"Pop val cannot be larger than len(message): {num} > {len(self.message)}")
        return self.message

    def clear(self):
        self.message = ""
        return self.message

    def send(self, message: str = None):
        if message:
            message += "\n"
            return self.bus.write(message.encode('utf-8'))

        if self.message:
            return self.bus.write(self.message.encode('utf-8'))

        print("No Message Exists")
        return 0

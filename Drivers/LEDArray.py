from .apa102 import APA102


class LEDArray:
    def __init__(self):
        self.idx = 0
        self.driver = APA102(3)

    def idle(self):
        """In the idle state, the LED is green"""
        self.driver.set_pixel(self.idx, 0, 255, 0, 10)
        self.driver.show()

    def speech(self):
        """While recording speech, the LED is blue"""
        self.driver.set_pixel(self.idx, 0, 0, 255, 10)
        self.driver.show()

    def gsr(self):
        """While sampling GSR, the LED is purple"""
        self.driver.set_pixel(self.idx, 255, 0, 255, 10)
        self.driver.show()

    def result(self, red, green):
        """The LED will be a different color based on the predicted emotion"""
        self.driver.set_pixel(self.idx, red, green, 0, 10)
        self.driver.show()
        pass

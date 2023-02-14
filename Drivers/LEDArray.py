from .apa102 import APA102

class LEDArray:
    def __int__(self, led: str):
        self.idx = 0
        self.driver = APA102(1)

    def idle(self):
        """In the idle state, the LED is green"""
        self.driver.set_pixel(self.idx, 0, 255, 0, 5)
        self.driver.show()

    def speech(self):
        """While recording speech, the LED is blue"""
        self.driver.set_pixel(self.idx, 0, 0, 255, 5)
        self.driver.show()

    def gsr(self):
        """While sampling GSR, the LED is white"""
        self.driver.set_pixel(self.idx, 0, 0, 0, 5)
        self.driver.show()

    def result(self):
        """The LED will be a different color based on the predicted emotion"""
        pass

import RPi.GPIO as GPIO
import time

class PushButton:
    def __init__(self):
        self.but = 17
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.but, GPIO.IN)

    def push(self):
        while True:
            state = GPIO.input(self.but)
            if state:
                print("off")
            else:
                print("on")
                break
            time.sleep(0.05)

    def is_pressed(self):
        return not GPIO.input(self.but)

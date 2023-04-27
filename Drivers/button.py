import RPi.GPIO as GPIO
import time

class button:
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

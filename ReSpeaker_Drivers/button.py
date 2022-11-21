# Written by Matteo Vidali
# Based off of https://github.com/respeaker/mic_hat/tree/master/interfaces/button.py
# In an attempt to make the button an object


import RPi.GPIO as GPIO
import time
from typing import Callable

# To use this class, you may only instantiate one button
# The on_button_func is the function you want to be called whe
# the button is pressed. 

#   @breif: Instantiates a button object linked to the button on the
#           ReSpeaker 2-mics Hat
#
#   @params:    on_button_func: Callable    - A function that will be called when the
#                                             button is pressed.
#               d_time: optional float      - A value for how long the button should
#                                             wait between polling.
#   @retval: None atm - perhaps boolean state of button later

class Button:
    def __init__(self, on_button_func: Callable, d_time: float = 1):
        self.pin = 17
        self.func = on_button_func
        self.down_time = d_time

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        
    def listen(self):
        while True:
            state = GPIO.input(self.pin)

            if state:
                print("OFF")

            else:
                self.func()
                
            time.sleep(self.down_time)
    


if __name__ == "__main__":

    def buttonCall():
        print("IM PRESSED!")

    button = Button(buttonCall)
    button.listen()

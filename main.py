from Data_Drivers import DataFlow, GSR
from ReSpeaker_Drivers import Mics, Button

def main():
    mic = Mics()
    gsr = GSR()

    df = DataFlow([gsr.read], True, True, 'test.out')
    button = Button(on_button_func=df.pause)


if __name__ == "__main__":
    main()
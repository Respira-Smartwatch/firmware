from Data_Drivers import DataFlow, GSR
from ReSpeaker_Drivers import Mics, Button

def main():
    mic = Mics()
    gsr = GSR()
    df = DataFlow([gsr.read], True, True, 'test.out')


if __name__ == "__main__":
    main()
import serial
import sys
#from Models import SpeechEmotionClassifier, GSRClassifier
from Models import GSRClassifier

_ser = None

def push_to_tty(*args) -> bool:
    global _ser
    if not _ser:
        try:
            _ser = serial.Serial("/dev/ttyS0",
                                 baudrate=9600,
                                 parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE,
                                 bytesize=serial.EIGHTBITS,
                                 timeout=1)
        except not _ser.is_open:
            print("ERROR: SERIAL PORT UNABLE TO OPEN!")
            return False

    for data in args:
        try:
            _ser.write(data.to_bytes(1, 'little'))
        except serial.SerialTimeoutException: 
            print("Serial Timeout while Writing...")
            return False
    
    return True
    

def main(plotting=False):

    #audio_classifier = SpeechEmotionClassifier()
    gsr_classifier = GSRClassifier()

    # completely arbitrary value that will need to be 
    # Set experimentally:
    gsr_gating_threshold = 25

    while True:
        anxiety_level = gsr_classifier.predict()

        emotion = None
        if anxiety_level >= gsr_gating_threshold:
            print("STARTING AUDIO CLASSIFIER")
            emotion=-1
            #emotion = audio_classifier.predict()
            pass
        
        print(f"Anxiety Level as given by GSR: {anxiety_level} / {gsr_gating_threshold}")
        if emotion:
            print(f"Emotion as given by SE Classifier: {emotion}")

        # Handles plotting via tty
        if plotting:
            complete = push_to_tty(anxiety_level, emotion)
            if not complete:
                print("Error while writing to serial port")
    

if __name__ == "__main__":
    main()

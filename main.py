from data import datacollection
from Drivers import LEDArray
from Models import GSRClassifier, SpeechEmotionClassifier
from timeit import default_timer as timer

def capture_speech(led0, model):
    led0.speech()
    emotions = model.predict()
    return emotions

def capture_gsr(led0, model):
    led0.gsr()
    phasic, tonic = model.predict()
    return phasic, tonic

if __name__ == "__main__":
    # Models
    gsr_model = GSRClassifier()
    speech_model = SpeechEmotionClassifier()
    
    # LED
    led = LEDArray()

    # Model parameters
    speech_duration_s = 5.0
    gsr_gating_threshold = 25

    while True:
        led.idle()
        cmd = input("> ")

        if cmd == "help" or cmd == "":
            print("Available commands:")
            print("speech: take a speech sample")
            print("gsr: take a gsr sample")
            print("data_collect: run data collection")
            print("data_debug: run data collection no input req")
            print("exit: exit program")

        elif cmd == "speech":
            emotions = capture_speech(led, speech_model)
            print(emotions)

        elif cmd == "gsr":
             phasic, tonic = capture_gsr(led, gsr_model)
             print(f"GSR Phasic:\t{phasic}")
             print(f"GSR Tonic:\t{tonic}")

        elif cmd == "data_collect":
            subject_name = input("Please enter subject name: ")
            datacollection(gsr_model, speech_model, subject_name)
        
        elif cmd == "data_debug":
            subject_name = input("Please enter subject name: ")
            datacollection(gsr_model, speech_model, subject_name, debug=True)

        elif cmd == "profile":
            gsr_time = 0
            for i in range(20):
                start = timer()
                _ = gsr_model.predict()
                end = timer()

                print(end - start, "sec")
                gsr_time += (end-start)

            print("Average GSR:", gsr_time / 20, "sec")

            speech_time = 0
            for i in range(20):
                start = timer()
                _ = speech_model.predict()
                end = timer()

                print(end - start, "sec")
                speech_time += (end-start)

            print("Average speech:", speech_time / 20, "sec")
        
        elif cmd == "exit":
            exit(0)

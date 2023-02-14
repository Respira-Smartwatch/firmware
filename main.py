from .data import datacollection
from Drivers import LEDArray
from Models import GSRClassifier, SpeechEmotionClassifier


def capture_speech(led0, model):
    led0.speech()
    pred = model.predict()
    print(pred)

    return pred


def capture_gsr(led0, model):
    led0.gsr()
    pred = model.predict()
    print(pred)

    return pred

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
        cmd = input()

        if cmd == "speech":
            _ = capture_speech(led, speech_model)

        elif cmd == "gsr":
            _ = capture_gsr(led, gsr_model)

        elif cmd == "data_collect":
            datacollection()

from Models import GSRClassifier, SpeechEmotionClassifier
from Drivers import APA102 

if __name__ == "__main__":
    # Models
    gsr_model = GSRClassifier()
    speech_model = SpeechEmotionClassifier()

    # LED (should be wrapped in new class)
    activity_led = 0
    gsr_led = 1
    speech_led = 2
    led = APA102(3)
    led.clear_strip()

    led.set_pixel(activity_led, 0, 255, 0, 5)
    led.show()

    # Model parameters
    speech_duration_s = 5.0
    gsr_gating_threshold = 25

    gsr_pred = gsr_model.predict()
    speech_model.predict()


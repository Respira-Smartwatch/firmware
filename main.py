from Models import GSRClassifier, SpeechEmotionClassifier

if __name__ == "__main__":
    # Models
    gsr_model = GSRClassifier()
    speech_model = SpeechEmotionClassifier()

    # Model parameters
    speech_duration_s = 5.0
    gsr_gating_threshold = 25

    gsr_pred = gsr_model.predict()
    speech_model.predict()


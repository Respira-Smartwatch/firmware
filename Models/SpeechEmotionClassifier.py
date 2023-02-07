import numpy as np
import sys

sys.path.insert(0, "./Models/speech-emotion-classifier/src")

from Drivers.AudioDriver import AudioDriver
from Respira import FeatureExtractor, EmotionClassifier


class SpeechEmotionClassifier:
    def __init__(self):
        self.model = EmotionClassifier("./Models/speech-emotion-classifier/results/respira-emoc.bin")
        self.audio = AudioDriver()

    def predict(self):
        samples = self.audio.get_sample()

        emission = FeatureExtractor.from_samples(samples, 16000)
        emission = np.hstack((emission["mfcc"], emission["chroma"], emission["mel"]))

        prediction, probabilities = self.model([emission])

        category = ["neutral", "calm", "happy", "sad", "angry", "fearful", "disgust", "surprise"][prediction[0]]
        probability = max(probabilities[0]) * 100

        print(f"{prediction} ({probability} %)")

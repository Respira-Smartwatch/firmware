import numpy as np
import sys

sys.path.insert(0, "./Models/speech-emotion-classifier/src")

from Drivers.AudioDriver import AudioDriver
from Respira import FeatureExtractor, EmotionClassifier


class SpeechEmotionClassifier:
    def __init__(self):
        self.model = EmotionClassifier("./Models/speech-emotion-classifier/results/respira-emoc.bin")
        self.audio = AudioDriver()

    def predict(self, sample_length_sec: float = 5.0) -> dict:
        samples = self.audio.get_sample(sample_length_sec)

        emission = FeatureExtractor.from_samples(samples, 16000)
        emission = np.hstack((emission["mfcc"], emission["chroma"], emission["mel"]))

        prediction, probabilities = self.model([emission])
        probabilities = probabilities[0]

        result = {
            "happy": probabilities[0] * 100.0,
            "sad": probabilities[1] * 100.0,
            "disgust": probabilities[2] * 100.0,
            "surprise": probabilities[3] * 100.0
        }

        return result

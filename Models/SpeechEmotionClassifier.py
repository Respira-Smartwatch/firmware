import sys
from typing import Union, Any

import numpy as np

sys.path.insert(0, "/home/pi/firmware/Models/speech-emotion-classifier/src")
sys.path.insert(0, "/home/pi/firmware/Drivers/")

from AudioDriver import AudioDriver
from Respira import FeatureExtractor, EmotionClassifier


class SpeechEmotionClassifier:
    def __init__(self):
        self.model = EmotionClassifier("/home/pi/firmware/Models/speech-emotion-classifier/results/respira-emoc.bin")
        self.audio = AudioDriver()

    def predict(self, sample_length_sec: float = 5.0) -> tuple[dict[str, Union[float]], Any]:
        samples = self.audio.get_sample(sample_length_sec)

        emission = FeatureExtractor.from_samples(samples, 16000)
        emission = np.hstack((emission["mfcc"], emission["chroma"], emission["mel"]))

        prediction, probabilities = self.model([emission])
        probabilities = probabilities[0]

        result = {
            "neutral": probabilities[0] * 100.0,
            "calm": probabilities[1] * 100.0,
            "happy": probabilities[2] * 100.0,
            "sad": probabilities[3] * 100.0,
            "angry": probabilities[4] * 100.0,
            "fearful": probabilities[5] * 100.0,
            "disgust": probabilities[6] * 100.0,
            "surprise": probabilities[7] * 100.0
        }

        return result, samples

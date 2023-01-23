import sys
import torch

sys.path.insert(0, "./Models/speech-emotion-classifier/src")

from Drivers.AudioDriver import AudioDriver
from Respira import FeatureExtractor, EmotionClassifier

class SpeechEmotionClassifier:
    def __init__(self):
        self.feature_extractor = FeatureExtractor()
        self.model = EmotionClassifier("./Models/speech-emotion-classifier/results/respira-emoc.bin")
        self.audio = AudioDriver()

    def predict(self):
        samples = torch.tensor([self.audio.get_sample()])

        features = self.feature_extractor.from_samples(samples)
        logits = self.model(features)

        logits = torch.mean(logits, dim=0).tolist()
        max_logit = logits.index(max(logits))

        categories = ["neutral", "calm", "happy", "sad", "angry", "fearful", "disgust", "surprise"]

        print(f"Probabilities:\n{categories}\n{logits}")
        print(f"Prediction: {categories[max_logit]}")


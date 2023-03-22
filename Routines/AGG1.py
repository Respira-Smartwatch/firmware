import sys

sys.path.insert(0, "/home/pi/firmware/Models")
sys.path.insert(0, "/home/pi/firmware/Drivers")
from GSRClassifier import GSRClassifier
from SpeechEmotionClassifier import SpeechEmotionClassifier
from LEDArray import LEDArray
import numpy as np

# Get GSR Precition
# Get Speech Prediction
# Combine these in some meaningful way to guage total stress
# GSR gives instant stress *(physiological)
# Speech gives psychological stress

class Aggregate:
    def __init__(self, threshold: int=5):
        self.gsr = GSRClassifier()
        self.speech = SpeechEmotionClassifier()
        self.led = LEDArray()
        self.threshold = threshold

    def predict(self, samples):
        #average tonic and phasic to make baseline
        #compare new values to previous baseline
        #if new value - baseline is > threshold, then activate speech classifier
        #both tonic and phasic have to be > threshold

        stress_eval = {"happy": 0.1, "sad": 0.35, "disgust": 0.75, "surprise": 1} #scalers for emotion to stress response on confidence value NOTE: UPDATES NEEDED TO FIND REAL STRESS CLASS LABEL ACCURACY
        val=0
        average = []
        ran = 0
        psamples = 0
        tsamples = 0
        tonicf = 0
        for s in range(samples):
            phasic, tonic = self.gsr.predict()
            average.append(tonic)
            #tsamples += tonic
            #tonicbl = tonic - (tsamples / (s + 1))
            if s % 5:
                for t in range(len(average)):
                    if t == 0:
                        diff = 0
                        val = 0
                    else:
                        val += average[t] - average[t-1]
                if ((np.max(average) - np.min(average)) > 0):
                    val = ((val/5) - np.min(average)) / (np.max(average) - np.min(average)) # normalize range for average tonic sample difference from 0 to 1
                average = []  

            #only runs speech classifier once during sampling
            if val > self.threshold and ran == 0:
                ran = 1
                speech_data,_ = self.speech.predict()
                maximum = speech_data['happy'] #default
                for key,value in speech_data.items():
                    if (value > maximum):
                        maximum = value
                        confid = maximum / 100
                        stress = stress_eval[key]
                        confid = (val) + (stress*confid) 
                #turn on LEDs based on new value
                print("confid: ", confid)
                self.LED(confid)

    def LED(self, confid):

        # assumes Confid is confidence score normalized 0-1 for how stress the individual is
        # Use normalized value 0-1 and multiply by 0-255 RGB scale (Usually will display orange/yellow)
        if (confid <= 0.25):
            red = int(255 * confid) # indicates stress
            green = int(255 - 255 * confid) # does not indicate stress
            self.led.result(red,green)
        elif (confid < 0.75 and confid > 0.25):
            red = int(255 * confid) # indicates stress
            if (confid < 0.5):    
                red += 40 # Make redder
                green = int(255 - 255 * confid) # does not indicate stress
            if (confid > 0.5):
                green += 40 # Make greener
                self.led.result(red,green)
        else: # confid >= 0.75
            if confid > 1:
                confid = 1
            red = int(255 * confid)  # indicates stress
            green = int(255 - 255 * confid) # does not indicate stress
            self.led.result(red,green)
        return 

if __name__ == "__main__":
    a = Aggregate()
    a.predict(30)


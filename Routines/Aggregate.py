import sys
import json
import datetime

sys.path.insert(0, "/home/pi/firmware/Models")
sys.path.insert(0, "/home/pi/firmware/Drivers")
from GSRClassifier import GSRClassifier
from SpeechEmotionClassifier import SpeechEmotionClassifier
from Drivers import LEDArray
import numpy as np
import time

class Aggregate:
    def __init__(self, gsr_model: GSRClassifier, speech_model: SpeechEmotionClassifier, ledarray: LEDArray):
        self.gsr = gsr_model # GSR gives instant stress *(physiological)
        self.speech = speech_model # Speech gives psychological stress
        self.led = ledarray
        self.threshold = 0
	
    @staticmethod
    def empty_sample_dict():
        return dict({
            "gsr_tonic": [],
            "speech_class": [],
            "speech_probability": [],
            "stress_score": []
        })

    def predict(self, samples: int):
        #average tonic to make baseline
        #compare new values to previous baseline
        #if new value - baseline is > threshold, then activate speech classifier
        #tonic has to be > threshold

        timestamp = str(datetime.datetime.now()).split(" ")[0]
        f"respira_{timestamp}.json"
        data = {
	        "date": timestamp
	    }

        stress_eval = {"happy": 0.1, "sad": 0.2, "disgust": 0.75, "surprise": 1} #scalers for emotion to stress response on confidence value NOTE: UPDATES NEEDED TO FIND REAL STRESS CLASS LABEL ACCURACY
        average = []  
        val = 0
        confid = 0 
        for s in range(samples):
            phasic, tonic = self.gsr.predict()
            average.append(tonic)
            av = sum(average)/len(average)
            if s % 5:
                for t in range(len(average)):
                    if t == 0:
                        ran = 0 # state machine to transition to speech recording
                        val = 0
                    else:
                        val += average[t] - average[t-1]
                if ((np.max(average) - np.min(average)) > 0):
                    val = ((val/5) - np.min(average)) / (np.max(average) - np.min(average)) # normalize range for average tonic sample difference from 0 to 1
                average = []  

            #only runs speech classifier once during sampling
            if abs(val) > self.threshold and ran == 0:
                print("\nReading Speech Data\n")
                ran = 1
                speech_data,_ = self.speech.predict()
                maximum = speech_data['happy'] #default
                for key,value in speech_data.items():
                    if (value >= maximum):
                        maximum = value
                        max_key = key
                        confid = maximum / 100
                        stress = stress_eval[key]
                        confid = (stress*confid) 
                #turn on LEDs based on new value
                self.LED(confid)
	   
            timestamp = str(datetime.datetime.now()).split(" ")[1]	 
            if confid:
                data[timestamp] = self.empty_sample_dict()
                data[timestamp]["gsr_tonic"] = av
                data[timestamp]["speech_key"] = max_key
                data[timestamp]["speech_probability"] = maximum
                data[timestamp]["stress_score"] = confid
            else:
                data[timestamp] = self.empty_sample_dict()
                data[timestamp]["gsr_tonic"] = av
                data[timestamp]["speech_key"] = 0
                data[timestamp]["speech_probability"] = 0
                data[timestamp]["stress_score"] = 0
                
        with open(filename, 'w') as fout:
            json_dumps_str = json.dumps(data, indent=4)
            print(json_dumps_str, file=fout)

    def LED(self, confid):
        # assumes Confid is confidence score normalized 0-1 for how stress the individual is
        # Use normalized value 0-1 and multiply by 0-255 RGB scale
        #confid of 1: red indicates stress
        #confid of 0: green does not indicate stress

        if confid > 1:
            confid = 1  
        green = 0
        red = 0
        
        if (confid <= 0.25):
            red = int(255 * confid) # indicates stress
            green = int(255 - (255 * confid)) # does not indicate stress
        elif (confid < 0.75 and confid > 0.25):
            red = int(255 * confid) # indicates stress
            green = int(255 - (255 * confid)) # does not indicate stress
            if (confid < 0.5):    
                green += 40 # Make more green
            if (confid > 0.5):
                red += 40 # Make more red
        else: # confid >= 0.75
            red = int(255 * confid)  # indicates stress
            green = int(255 - (255 * confid)) # does not indicate stress
        self.led.result(red, green)
        return 
        

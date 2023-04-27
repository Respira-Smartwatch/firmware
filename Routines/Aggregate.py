import datetime
import json
import sys

sys.path.insert(0, "/home/pi/firmware/Models")
sys.path.insert(0, "/home/pi/firmware/Drivers")
from GSRClassifier import GSRClassifier
from SpeechEmotionClassifier import SpeechEmotionClassifier
from Drivers import LEDArray
import numpy as np


class Aggregate:
    def __init__(self, gsr_model: GSRClassifier, speech_model: SpeechEmotionClassifier, ledarray: LEDArray):
        self.gsr = gsr_model  # GSR gives instant stress *(physiological)
        self.speech = speech_model  # Speech gives psychological stress
        self.led = ledarray
        self.threshold = 3

    @staticmethod
    def empty_sample_dict():
        return dict({
            "average_gsr_tonic": [],
            "speech_class": [],
            "speech_probability": [],
            "stress_score": []
        })

    def predict(self, samples: int, should_export: bool = True):
        # average tonic to make baseline
        # compare new values to previous baseline
        # if new value - baseline is > threshold, then activate speech classifier
        # tonic has to be > threshold

        timedate = str(datetime.datetime.now()).split(" ")[0]
        filetime = str(datetime.datetime.now()).split(" ")[1]
        filename = f"respira_{timedate}_{filetime}.json"
        data = {
            "title": "Respira",
            "date": timedate
        }

        stress_eval = {"calm": 0.0, "happy": 0.25, "neutral": 0.5, "sad": 0.75, "fearful": 0.45, "angry": 0.65, "surprise": 0.60, "disgust": 0.70}  # scales confidence
        # NEEDED TO FIND REAL STRESS CLASS LABEL ACCURACY
        average = []
        val = 0
        confid = 0
        for s in range(samples): # Actual sample size approach
            ran = 0
            phasic, tonic, _ = self.gsr.predict()
            average.append(tonic)
            av = sum(average)/len(average)

            # CMNDF
            diff = [0] * len(average)
            for i in range(len(average)):
                for j in range(len(average) - i):
                    diff[i] = pow(average[j] - average[j+i], 2)
                    
            cmndf = [0] * len(average)
            cmndf[0] = 1

            for i in range(1, len(diff)):
                dsum = 0
            
                for j in range(1, i+1):
                    dsum += diff[j]
                    
                cmndf[i] = diff[i] * (i / dsum)

            #derivative function for cmndf
            #can possibly optimize by finding slope from previous value
            dt = 1.0
            dcf = [0] * len(average)
            dcf = np.diff(cmndf) / dt
            dcf = np.insert(dcf, 0, 0)

            val = dcf[s]

            # only runs speech classifier once during sampling
            if abs(val) > self.threshold and ran == 0:
                print("\nReading Speech Data\n")
                ran = 1
                speech_data, _ = self.speech.predict()
                sig_count = 0 # number of significant speech outputs
                stress = 0 # weight accumulation
                maximum = 0  # probability accumulation
                max_val = 0 # default maximum probability
                for key, value in speech_data.items():
                    print(key, value)
                    if (value >= max_val):
                        max_val = value
                        max_key = key
                    if (value >= 80): # large probabilities 80%
                        maximum = value
                        stress = stress_eval[key] # weights
                        sig_count += 1
                    elif (value < 80 and value >= 35): # small probabilities 35%
                        maximum += value
                        stress += stress_eval[key] # weights
                        sig_count += 1
                confid = (maximum/sig_count) / 100
                confid = (stress/sig_count) * confid

                # turn on LEDs based on new value
                self.LED(confid)

            if should_export:
                timestamp = str(datetime.datetime.now()).split(" ")[1]
                if ran:
                    data[timestamp] = self.empty_sample_dict()
                    data[timestamp]["average_gsr_tonic"] = av
                    data[timestamp]["speech_class"] = max_key
                    data[timestamp]["speech_probability"] = max_val
                    data[timestamp]["stress_score"] = confid
                else:
                    data[timestamp] = self.empty_sample_dict()
                    data[timestamp]["average_gsr_tonic"] = av
                    data[timestamp]["speech_class"] = 0
                    data[timestamp]["speech_probability"] = 0
                    data[timestamp]["stress_score"] = 0

        if should_export:
            with open(filename, 'w') as fout:
                json_dumps_str = json.dumps(data, indent=4)
                print(json_dumps_str, file=fout)

    def LED(self, confid):
        # assumes Confid is confidence score normalized 0-1 for how stress the individual is
        # Use normalized value 0-1 and multiply by 0-255 RGB scale 
        # confid of 1: red indicates stress
        # confid of 0: green does not indicate stress

        if confid > 1:
            confid = 1
        green = 0
        red = 0

        if confid <= 0.25:
            red = int(255 * confid)  # indicates stress
            green = int(255 - (255 * confid))  # does not indicate stress
        elif 0.75 > confid > 0.25:
            red = int(255 * confid)  # indicates stress
            green = int(255 - (255 * confid))  # does not indicate stress
            if (confid < 0.5) and (green < 210):
                green += 40  # Make more green
            if (confid > 0.5) and (red < 210):
                red += 40  # Make more red
        else:  # confid >= 0.75
            red = int(255 * confid)  # indicates stress
            green = int(255 - (255 * confid))  # does not indicate stress
        self.led.result(red, green)
        print("LED Values: Red: ", red, "Green: ", green)
        return

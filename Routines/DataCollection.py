import asyncio
import datetime
import json
import time
import sys
import serial
from .pychartPusher import PychartPusher

from Drivers import LEDArray
from Models import GSRClassifier, SpeechEmotionClassifier
from multiprocessing import Process

_TTY_BUS = serial.Serial("/dev/ttyS0", baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                         bytesize=serial.EIGHTBITS, timeout=1)


def push_to_tty(values: list):
    data = ','.join(values)
    _TTY_BUS.write(data.to_bytes(1, 'little'))
    return 1


class DataCollection:
    def __init__(self, gsr_model: GSRClassifier, speech_model: SpeechEmotionClassifier):
        self._GSR_MODEL = gsr_model
        self._SPEECH_MODEL = speech_model
        self.led = LEDArray()
        self.PP = PychartPusher()

        self.lock = asyncio.Lock()

    def sample_gsr(self, gsr_array):
        while True:
            phasic, tonic = self._GSR_MODEL.predict()

            with self.lock:
                gsr_array.append([phasic, tonic])

    def sample_speech(self, speech_array):
        while True:
            prob, samples = self._SPEECH_MODEL.predict(2.75)
            prob = list(prob.values())
            samples = list(samples)

            with self.lock:
                speech_array.append([prob[0], prob[1], prob[2], prob[3], samples])

    def run_prediction(self, data: dict, test_name: str, gsr: bool, speech: bool, time_s: float):
        self.led.idle()

        # Multiprocessing data structures
        gsr_array = []
        speech_array = []

        gsr_p = Process(target=self.sample_gsr, args=(gsr_array,))
        speech_p = Process(target=self.sample_speech, args=(speech_array,))

        # Sample before time runs out
        start_time = time.time()
        gsr_p.start()
        speech_p.start()

        while time.time() - start_time <= time_s:
            continue

        # When time runs out, kill threads as long as they are not writing
        with self.lock:
            gsr_p.terminate()
            speech_p.terminate()

            # Store results
            # Setup test fields
            data[test_name] = {
                "gsr_phasic": [x[0] for x in gsr_array],
                "gsr_tonic": [x[1] for x in gsr_array],

                "speech_happy": [x[0] for x in speech_array],
                "speech_sad": [x[1] for x in speech_array],
                "speech_disgust": [x[2] for x in speech_array],
                "speech_surprise": [x[3] for x in speech_array],

                "speech_samples": [x[4] for x in speech_array],
                "stress_rating": 0
            }

        self.led.idle()
        return time.time() - start_time

    def run(self, subject_name: str, debug=False):
        s = time.time()
        debug_time = 0

        timestamp = str(datetime.datetime.now()).split(" ")[0]
        filename = f"respira_{subject_name}_{timestamp}.json"

        data = {
            "subject": subject_name,
            "date": timestamp
        }

        debug_time = t = s - time.time()

        print(f"debug_time so far: {debug_time}")  # DEBUG

        # TEST BEGIN  ---------------------------------------------

        # Test Structure:
        # 01. Video Beginning: (8s) rest
        # 02. First Baseline: 2 readings (15s each), speech & gsr
        # 03. Reading time: (8s) rest
        # 04. Expiration test 1: 4 readings (15s each), gsr
        # 05. Reading time: (10s) rest
        # 06. Rest 1: 2 readings (15s each), gsr
        # 07. Reading time: (8s) rest
        # 08. Expiration test 2: 4 readings (15s each), gsr
        # 09. Reading time: (8s) rest
        # 10. Rest 2: 2 readings (15s each), gsr
        # 11. Reading time: (8s) rest
        # 12. Video Test #3: 10 readings (15s each), gsr
        # 13. Reading time: (9s) rest
        # 14. Rest 3: 2 readings (15s each), gsr
        # 15. Reading time: (6s) rest
        # 16. Reciting Test #4: 2 readings (15s each) speech & gsr
        # 17. Reading time: (5s) rest
        # 18. Rest #4: 2 readings (15s each) gsr

        # Beginning of Video -------------------------------------
        if not debug:
            time.sleep(8 - t)
        print(f"Intro Time: {time.time() - s}")  # DEBUG

        # First Baseline Test ------------------------------------
        print("Baseline Test")

        t = 0  # DEBUG
        t += self.run_prediction(data, "baseline", True, True, 15)

        print(f"End of Baseline Test (time: {t}s)")

        # Reading time ------------------------------------------
        if not debug:
            time.sleep(8)  # 0:38 - 0:46

        # Expiration Test #1 ------------------------------------
        print("Expiration Test #1")

        t += self.run_prediction(data, "expiration1", True, False, 15)

        print(f"End of Expiration Test (time: {t}s)")

        # Reading time ------------------------------------------
        if not debug:
            time.sleep(10)  # 1:46 - 1:56
            stress = input("Enter stress level rating 0-5: ")
        else:
            stress = -1

        data["expiration1"]["stress_rating"] = int(stress)

        # Rest #1 -----------------------------------------------
        print("Rest #1")
        t += self.run_prediction(data, "rest1", True, False, 15)

        print(f"End of Rest #1 (time: {t}s)")

        # Reading time ------------------------------------------
        if not debug:
            time.sleep(8)  # 2:26 - 2:34

        # Expiration Test #2 ------------------------------------
        print("Expiration Test #2")

        t += self.run_prediction(data, "expiration2", True, False, 15)

        print(f"End of Expiration #2 Test (time: {t}s)")

        # Reading time ------------------------------------------
        if not debug:
            time.sleep(8)  # 3:34 - 3:42
            stress = input("Enter stress level rating 0-5: ")
        else:
            stress = -1

        data["expiration2"]["stress_rating"] = int(stress)

        # Rest #2 -----------------------------------------------
        print("Rest #2")

        t += self.run_prediction(data, "rest2", True, False, 15)

        print(f"End of Rest #2 (time: {t}s)")

        # Reading time ------------------------------------------
        if not debug:
            time.sleep(8)  # 4:12 - 4:20

        # Video Test #3 -----------------------------------------
        print("Video Test #3")

        t += self.run_prediction(data, "video", True, False, 15)

        print(f"End of Video Test. (time: {t})")

        # Reading time -----------------------------------------
        if not debug:
            time.sleep(9)  # 6:50 - 6:59
            stress = input("Enter stress level rating 0-5: ")
        else:
            stress = -1

        data["video"]["stress_rating"] = int(stress)

        # Rest #3 ----------------------------------------------
        print("Rest #3")

        t += self.run_prediction(data, "rest3", True, False, 15)

        print(f"End of Rest #3 (time: {t}s)")

        # Reading time -----------------------------------------
        if not debug:
            time.sleep(6)  # 7:29 - 7:35

        # Reciting Test #4 -------------------------------------
        print("Reciting Test #4")

        t += self.run_prediction(data, "recitation", True, True, 15)

        print(f"End of Reciting Test #4 (time: {t}s)")

        # Reading time -----------------------------------------
        if not debug:
            time.sleep(5)  # 8:05 - 8:10
            stress = input("Enter stress level rating 0-5: ")
        else:
            stress = -1

        data["recitation"]["stress_rating"] = int(stress)

        # Rest #4 ----------------------------------------------
        print("Rest #4")

        t += self.run_prediction(data, "rest4", True, False, 15)

        print(f"End of Rest #4 (time: {t}s)")

        # TEST FINISHED ---------------------------------------!

        # File writing and test end ----------------------------
        with open(filename, 'w') as fout:
            json_dumps_str = json.dumps(data, indent=4)
            print(json_dumps_str, file=fout)

        debug_time += t

        print("End of data collection protocol")
        print(f"Total Time to complete: {time.time() - s}s")
        print(f"Total prediction time computed: {debug_time}s")

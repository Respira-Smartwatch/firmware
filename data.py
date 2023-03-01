import copy
import datetime
import json
import time

from Drivers import LEDArray

_GSR_MODEL = None
_SPEECH_MODEL = None
_FILE_WRITER = None


def run_prediction(data: dict, test_name: str, 
                   gsr: bool, speech: bool, 
                   time_s: float, num_runs: int, 
                   debug: bool=False):

    global _GSR_MODEL, _SPEECH_MODEL

    if not (_GSR_MODEL and _SPEECH_MODEL):
        print("NO GLOBALS DEFINED")
        exit(1)

    led = LEDArray()
    led.idle()

    data[test_name] = {
        "gsr_phasic": [],
        "gsr_tonic": [],
        "speech_happy": [],
        "speech_sad": [],
        "speech_disgust": [],
        "speech_surprise": [],
        "stress_rating": 0
    }

    t_time = 0

    # Each run lasts for 'time_s' amount of time right now
    #    
    for _ in range(num_runs):
        s = time.time()

        led.gsr()
        for i in range(5):
            phasic, tonic = _GSR_MODEL.predict() if gsr else (-1,-1)
            data[test_name]["gsr_phasic"].append(phasic)
            data[test_name]["gsr_tonic"].append(tonic)

        led.speech()
        for i in range(5):
            prob = list(_SPEECH_MODEL.predict(1).values()) if speech else [-1, -1, -1, -1]
            data[test_name]["speech_happy"].append(prob[0])
            data[test_name]["speech_sad"].append(prob[1])
            data[test_name]["speech_disgust"].append(prob[2])
            data[test_name]["speech_surprise"].append(prob[3])

        led.gsr()
        for i in range(5):
            phasic, tonic = _GSR_MODEL.predict() if gsr else (0, 0)
            data[test_name]["gsr_phasic"].append(phasic)
            data[test_name]["gsr_tonic"].append(tonic)

        led.idle()

        t = time.time() - s

        if t < time_s and not debug:
            time.sleep(time_s - t)

        t_time += time.time()-s

    return t_time


def datacollection(gsr_model, speech_model, subject_name, debug=False):
    global _GSR_MODEL, _SPEECH_MODEL
    _GSR_MODEL = gsr_model
    _SPEECH_MODEL = speech_model

    s = time.time()
    debug_time = 0 

    timestamp = str(datetime.datetime.now()).split(" ")[0]
    filename = f"respira_{subject_name}_{timestamp}.json"

    data = {
        "subject": subject_name,
        "date": timestamp
    }

    debug_time = t = s-time.time()

    print(f"debug_time so far: {debug_time}") # DEBUG

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
        time.sleep(8-t)
    print(f"Intro Time: {time.time() - s}") # DEBUG

    # First Baseline Test ------------------------------------
    print("Baseline Test")

    t = 0 # DEBUG
    t += run_prediction(data, "baseline", True, True, 15, 2, debug)
    
    print(f"End of Baseline Test (time: {t}s)")

    # Reading time ------------------------------------------
    if not debug:
        time.sleep(8)# 0:38 - 0:46

    # Expiration Test #1 ------------------------------------
    print("Expiration Test #1")

    t += run_prediction(data, "expiration1", True, False, 15, 4, debug)

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
    t += run_prediction(data, "rest1", True, False, 15, 2, debug)

    print(f"End of Rest #1 (time: {t}s)")

    # Reading time ------------------------------------------
    if not debug:
        time.sleep(8)  # 2:26 - 2:34

    # Expiration Test #2 ------------------------------------
    print("Expiration Test #2")

    t += run_prediction(data, "expiration2", True, False, 15, 4, debug)

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

    t += run_prediction(data, "rest2", True, False, 15, 2, debug)

    print(f"End of Rest #2 (time: {t}s)")

    # Reading time ------------------------------------------
    if not debug:
        time.sleep(8)  # 4:12 - 4:20

    # Video Test #3 -----------------------------------------
    print("Video Test #3")

    t += run_prediction(data, "video", True, False, 15, 10, debug)

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

    t += run_prediction(data, "rest3", True, False, 15, 2, debug)

    print(f"End of Rest #3 (time: {t}s)")

    # Reading time -----------------------------------------
    if not debug:
        time.sleep(6)  # 7:29 - 7:35

    # Reciting Test #4 -------------------------------------
    print("Reciting Test #4")

    t += run_prediction(data, "recitation", True, True, 15, 2, debug)

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

    t += run_prediction(data, "rest4", True, False, 15, 2, debug)

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

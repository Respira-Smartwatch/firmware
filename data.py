import copy
import datetime
import json
import time

_GSR_MODEL = None
_SPEECH_MODEL = None
_FILE_WRITER = None

def run_prediction(gsr: bool, speech: bool, time_s: float, stress: list=[0]):
    s = time.time()
    global _GSR_MODEL, _SPEECH_MODEL, _FILE_WRITER

    if not (_GSR_MODEL and _SPEECH_MODEL and _FILE_WRITER):
        print("NO GLOBALS DEFINED")
        exit(1)

    phasic, tonic = _GSR_MODEL.predict() if gsr else 0,0
    prob = list(_SPEECH_MODEL.predict().values()) if speech else [0, 0, 0, 0]
    
    _FILE_WRITER.writerow([phasic, tonic] + prob + stress)
    
    t = time.time() - s
    if t < time_s:
        time.sleep(time_s - t)

    return phasic, tonic, prob, time.time()-s


def datacollection(gsr_model, speech_model, subject_name, with_input=True):
    s = time.time()
    debug_time = 0 

    timestamp = str(datetime.datetime.now()).split(" ")[0]
    filename = f"respira_{subject_name}_{timestamp}.json"

    data = {
        "subject": subject_name,
        "date": str(time)
    }

    data_fields = {
        "gsr_phasic": [],
        "gsr_tonic": [],
        "speech_happy": [],
        "speech_sad": [],
        "speech_disgust": [],
        "speech_surprise": [],
        "stress_rating": 0
    }

    global _GSR_MODEL, _SPEECH_MODEL, _FILE_WRITER
    _GSR_MODEL = gsr_model
    _SPEECH_MODEL = speech_model

    debug_time = t = s-time.time()

    print(f"debug_time so far: {debug_time}") # DEBUG

    # Beginning of Video
    time.sleep(8-t)

    print(f"Intro Time: {time.time() - s}") # DEBUG

    # First Baseline Test
    print("Baseline Test")
    data["baseline"] = copy.deepcopy(data_fields)

    t = [] # DEBUG
    for _ in range(2):
        phasic, tonic, prob, tp = run_prediction(True, True, 15)

        data["baseline"]["gsr_phasic"].append(phasic)
        data["baseline"]["gsr_tonic"].append(tonic)
        data["baseline"]["speech_happy"].append(prob[0])
        data["baseline"]["speech_sad"].append(prob[1])
        data["baseline"]["speech_disgust"].append(prob[2])
        data["baseline"]["speech_rating"].append(prob[3])

        t += tp,
    
    #DEBUG
    print(f"End of Baseline Test (time: {t}s)")
    debug_time += sum(t)

    # Reading time
    time.sleep(8)# 0:38 - 0:46

    # Expiration Test #1
    print("Expiration Test #1")
    data["expiration1"] = copy.deepcopy(data_fields)

    t = [] # DEBUG
    for _ in range(4):
        phasic, tonic, prob, tp = run_prediction(True, False, 15)

        data["expiration1"]["gsr_phasic"].append(phasic)
        data["expiration1"]["gsr_tonic"].append(tonic)
        data["expiration1"]["speech_happy"].append(prob[0])
        data["expiration1"]["speech_sad"].append(prob[1])
        data["expiration1"]["speech_disgust"].append(prob[2])
        data["expiration1"]["speech_rating"].append(prob[3])

        t += tp,

    print(f"End of Expiration Test (time: {t}s)")
    debug_time += sum(t)

    # Reading time
    time.sleep(10)  # 1:46 - 1:56

    # Rest #1
    print("Rest #1")
    stress = input("Enter stress level rating 0-5: ") if with_input else -1
    data["expiration1"]["stress_rating"] = int(stress)
    data["rest1"] = copy.deepcopy(data_fields)

    t = []
    for _ in range(2):
        phasic, tonic, prob, tp = run_prediction(True, False, 15, stress=[stress])

        data["rest1"]["gsr_phasic"].append(phasic)
        data["rest1"]["gsr_tonic"].append(tonic)
        data["rest1"]["speech_happy"].append(prob[0])
        data["rest1"]["speech_sad"].append(prob[1])
        data["rest1"]["speech_disgust"].append(prob[2])
        data["rest1"]["speech_rating"].append(prob[3])

        t += tp, 

    print(f"End of Rest #1 (time: {t}s)")
    debug_time += sum(t)

    # Reading time
    time.sleep(8)  # 2:26 - 2:34

    # Expiration Test #2
    print("Expiration Test #2")
    data["expiration2"] = copy.deepcopy(data_fields)

    t = []
    for _ in range(4):
        phasic, tonic, prob, tp = run_prediction(True, False, 15)

        data["expiration2"]["gsr_phasic"].append(phasic)
        data["expiration2"]["gsr_tonic"].append(tonic)
        data["expiration2"]["speech_happy"].append(prob[0])
        data["expiration2"]["speech_sad"].append(prob[1])
        data["expiration2"]["speech_disgust"].append(prob[2])
        data["expiration2"]["speech_rating"].append(prob[3])

        t += tp,

    print(f"End of Expiration #2 Test (time: {t}s)")
    debug_time += sum(t)

    # Reading time
    time.sleep(8)  # 3:34 - 3:42

    # Rest #2
    print("Rest #2")
    stress = input("Enter stress level rating 0-5: ") if with_input else -1
    data["expiration2"]["stress_rating"] = int(stress)
    data["rest2"] = copy.deepcopy(data_fields)

    t = []
    for _ in range(2):
        phasic, tonic, prob, tp = run_prediction(True, False, 15, stress=[stress])

        data["rest2"]["gsr_phasic"].append(phasic)
        data["rest2"]["gsr_tonic"].append(tonic)
        data["rest2"]["speech_happy"].append(prob[0])
        data["rest2"]["speech_sad"].append(prob[1])
        data["rest2"]["speech_disgust"].append(prob[2])
        data["rest2"]["speech_rating"].append(prob[3])

        t += tp,
    print(f"End of Rest #2 (time: {t}s)")
    debug_time += sum(t)

    # Reading time
    time.sleep(8)  # 4:12 - 4:20

    # Video Test #3
    print("Video Test #3")
    data["video"] = copy.deepcopy(data_fields)

    t = []
    for _ in range(10):
        phasic, tonic, prob, tp = run_prediction(True, False, 15)

        data["video"]["gsr_phasic"].append(phasic)
        data["video"]["gsr_tonic"].append(tonic)
        data["video"]["speech_happy"].append(prob[0])
        data["video"]["speech_sad"].append(prob[1])
        data["video"]["speech_disgust"].append(prob[2])
        data["video"]["speech_rating"].append(prob[3])

        t += tp,

    print(f"End of Video Test. (time: {t})")
    debug_time += sum(t)

    # Reading time
    time.sleep(9)  # 6:50 - 6:59

    # Rest #3
    print("Rest #3")
    stress = input("Enter stress level rating 0-5: ") if with_input else -1
    data["video"]["stress_rating"] = int(stress)
    data["rest3"] = copy.deepcopy(data_fields)

    t = []
    for i in range(2):
        phasic, tonic, prob, tp = run_prediction(True, False, 15, stress=[stress])

        data["rest3"]["gsr_phasic"].append(phasic)
        data["rest3"]["gsr_tonic"].append(tonic)
        data["rest3"]["speech_happy"].append(prob[0])
        data["rest3"]["speech_sad"].append(prob[1])
        data["rest3"]["speech_disgust"].append(prob[2])
        data["rest3"]["speech_rating"].append(prob[3])

        t += tp,

    print(f"End of Rest #3 (time: {t}s)")
    debug_time += sum(t)

    # Reading time
    time.sleep(6)  # 7:29 - 7:35

    # Reciting Test #4
    print("Reciting Test #4")
    data["recitation"] = copy.deepcopy(data_fields)

    t = []
    for _ in range(2):
        phasic, tonic, prob, tp = run_prediction(True, True, 15)

        data["recitation"]["gsr_phasic"].append(phasic)
        data["recitation"]["gsr_tonic"].append(tonic)
        data["recitation"]["speech_happy"].append(prob[0])
        data["recitation"]["speech_sad"].append(prob[1])
        data["recitation"]["speech_disgust"].append(prob[2])
        data["recitation"]["speech_rating"].append(prob[3])

        t += tp,
    print(f"End of Reciting Test #4 (time: {t}s)")
    debug_time += sum(t)

    # Reading time
    time.sleep(5)  # 8:05 - 8:10

    # Rest #4
    print("Rest #4")
    stress = input("Enter stress level rating 0-5: ") if with_input else -1
    data["recitation"]["stress_rating"] = int(stress)
    data["rest4"] = copy.deepcopy(data_fields)

    t = []
    for i in range(2):
        phasic, tonic, prob, tp = run_prediction(True, False, 15, [stress])
        t += tp,
    print(f"End of Rest #4 (time: {t}s)")
    debug_time += sum(t)

    with open(filename, 'w') as fout:
        json_dumps_str = json.dumps(data, indent=4)
        print(json_dumps_str, file=fout)

    print("End of data collection protocol")
    print(f"Total Time to complete: {time.time() - s}s")
    print(f"Total prediction time computed: {debug_time}s")

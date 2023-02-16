import csv
import datetime
import time

_GSR_MODEL = None
_SPEECH_MODEL = None
_FILE_WRITER = None

def run_prediction(gsr: bool, speech: bool, time_s: float, stress: list=[0])
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


def datacollection(gsr_model, speech_model, subject_name):
    
    s = time.time()

    timestamp = str(datetime.datetime.now()).split(" ")[0]
    filename = f"respira_{subject_name}_{timestamp}.csv"

    global _GSR_MODEL, _SPEECH_MODEL, _FILE_WRITER
    _GSR_MODEL = gsr_model
    _SPEECH_MODEL = speech_model
    of = open(filename, "w", newline='')
    writer = csv.writer(of)
    _FILE_WRITER = writer

    # Write Headers
    writer.writerow(["GSR Phasic",
                         "GSR Tonic",
                         "Speech Happy",
                         "Speech Sad",
                         "Speech Disgust",
                         "Speech Surprise",
                         "Stress rating"])
    
    t = s-time.time()
    # Beginning of Video
    time.sleep(8-t)

    # First Baseline Test
    print("Baseline Test")
    for _ in range(2):
        phasic, tonic, prob = run_prediction(True, True, 15)
    print("End of Baseline Test")

    # Reading time
    time.sleep(8)# 0:38 - 0:46

    # Expiration Test #1
    print("Expiration Test #1")
    for _ in range(4):
        phasic, tonic, prob = run_prediction(True, False, 15)
    print("End of Expiration Test")

    # Reading time
    time.sleep(10)  # 1:46 - 1:56

    # Rest #1
    print("Rest #1")
    stress = input("Enter stress level rating 0-5: ")

    for _ in range(2):
        phasic, tonic, prob = run_prediction(True, False, 15, stress=[stress])
    print("End of Rest #1")

    # Reading time
    time.sleep(8)  # 2:26 - 2:34

    # Expiration Test #2
    print("Expiration Test #2")
    for _ in range(4):
        phasic, tonic, prob = run_prediction(True, False, 15)
    print("End of Expiration #2 Test")

    # Reading time
    time.sleep(8)  # 3:34 - 3:42

    # Rest #2
    print("Rest #2")
    stress = input("Enter stress level rating 0-5: ")

    for _ in range(2):
        phasic, tonic, prob = run_prediction(True, False, 15, stress=[stress])
    print("End of Rest #2")

    # Reading time
    time.sleep(8)  # 4:12 - 4:20

    # Video Test #3
    print("Video Test #3")
    for _ in range(10):
        phasic, tonic, prob = run_prediction(True, False, 15)
    print("End of Video Test")

    # Reading time
    time.sleep(9)  # 6:50 - 6:59

    # Rest #3
    print("Rest #3")
    stress = input("Enter stress level rating 0-5: ")

    for i in range(2):
        phasic, tonic, prob = run_prediction(True, False, 15, stress=[stress])
    print("End of Rest #3")

    # Reading time
    time.sleep(6)  # 7:29 - 7:35

    # Reciting Test #4
    print("Reciting Test #4")
    for i in range(2):
        phasic, tonic, prob = run_prediction(True, True, 15)
    print("End of Reciting Test #4")

    # Reading time
    time.sleep(5)  # 8:05 - 8:10

    # Rest #4
    print("Rest #4")
    stress = input("Enter stress level rating 0-5: ")

    for i in range(2):
        phasic, tonic, prob = run_prediction(True, False, 15, [stress])
    print("End of Rest #4")

    of.close()

    print("End of data collection protocol")

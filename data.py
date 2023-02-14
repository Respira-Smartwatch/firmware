import csv
import datetime
import time


def datacollection(gsr_model, speech_model, subject_name):
    timestamp = str(datetime.datetime.now()).split(" ")[0]
    filename = f"respira_{subject_name}_{timestamp}.csv"

    with open(filename, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["GSR Phasic",
                         "GSR Tonic",
                         "Speech Happy",
                         "Speech Sad",
                         "Speech Disgust",
                         "Speech Surprise",
                         "Stress rating"])

        # Beginning of Video
        time.sleep(8)

        # First Baseline Test
        print("Baseline Test")
        for i in range(2):
            time.sleep(15)
            phasic, tonic = gsr_model.predict()
            prob = list(speech_model.predict().values())
            writer.writerow([phasic, tonic] + prob + [0])
        print("End of Baseline Test")

        # Reading time
        time.sleep(8)  # 0:38 - 0:46

        # Expiration Test #1
        print("Expiration Test #1")
        for i in range(4):
            time.sleep(15)
            phasic, tonic = gsr_model.predict()
            prob = list(speech_model.predict().values())
            writer.writerow([phasic, tonic] + prob + [0])
        print("End of Expiration Test")

        # Reading time
        time.sleep(10)  # 1:46 - 1:56

        # Rest #1
        print("Rest #1")
        stress = input("Enter stress level rating 0-5: ")

        for i in range(2):
            time.sleep(15)
            phasic, tonic = gsr_model.predict()
            prob = list(speech_model.predict().values())
            writer.writerow([phasic, tonic] + prob + [stress])
        print("End of Rest #1")

        # Reading time
        time.sleep(8)  # 2:26 - 2:34

        # Expiration Test #2
        print("Expiration Test #2")
        for i in range(4):
            time.sleep(15)
            phasic, tonic = gsr_model.predict()
            prob = list(speech_model.predict().values())
            writer.writerow([phasic, tonic] + prob + [0])
        print("End of Expiration #2 Test")

        # Reading time
        time.sleep(8)  # 3:34 - 3:42

        # Rest #2
        print("Rest #2")
        stress = input("Enter stress level rating 0-5: ")

        for i in range(2):
            time.sleep(15)
            phasic, tonic = gsr_model.predict()
            prob = list(speech_model.predict().values())
            writer.writerow([phasic, tonic] + prob + [stress])
        print("End of Rest #2")

        # Reading time
        time.sleep(8)  # 4:12 - 4:20

        # Video Test #3
        print("Video Test #3")
        for i in range(10):
            time.sleep(15)
            phasic, tonic = gsr_model.predict()
            prob = list(speech_model.predict().values())
            writer.writerow([phasic, tonic] + prob + [0])
        print("End of Video Test")

        # Reading time
        time.sleep(9)  # 6:50 - 6:59

        # Rest #3
        print("Rest #3")
        stress = input("Enter stress level rating 0-5: ")

        for i in range(2):
            time.sleep(15)
            phasic, tonic = gsr_model.predict()
            prob = list(speech_model.predict().values())
            writer.writerow([phasic, tonic] + prob + [stress])
        print("End of Rest #3")

        # Reading time
        time.sleep(6)  # 7:29 - 7:35

        # Reciting Test #4
        print("Reciting Test #4")
        for i in range(2):
            time.sleep(15)
            phasic, tonic = gsr_model.predict()
            prob = list(speech_model.predict().values())
            writer.writerow([phasic, tonic] + prob + [0])
        print("End of Reciting Test #4")

        # Reading time
        time.sleep(5)  # 8:05 - 8:10

        # Rest #4
        print("Rest #4")
        stress = input("Enter stress level rating 0-5: ")

        for i in range(2):
            time.sleep(15)
            phasic, tonic = gsr_model.predict()
            prob = list(speech_model.predict().values())
            writer.writerow([phasic, tonic] + prob + [stress])
        print("End of Rest #4")

    print("End of data collection protocol")

import csv
import time
from Models import GSRClassifier, SpeechEmotionClassifier
from Drivers import APA102

def datacollection():
   gsr_model = GSRClassifier()
   speech_model = SpeechEmotionClassifier()
   led = APA102(3)
   led.clear_strip()
   led.set_pixel(0, 255, 255, 255, 4) #Turn light to white
   led.show()

   with open('data_subject_0.csv', 'w', newline='') as file:
      writer = csv.writer(file)

      # Beginning of Video
      time.sleep(8)

      # First Baseline Test
      name = input("Enter your name: ")
      writer.writerow([name])
      writer.writerow(["GSR Phasic", "GSR Tonic", "Speech", "Speech Probability", "Stress Level"])
      writer.writerow(['First Baseline Test'])
      for i in range(2):
         time.sleep(15)
         phasic, tonic = gsr_model.predict() #Change to actual output 
         speech, prob = speech_model.predict() #Change to actual output
         writer.writerow([phasic, tonic, speech, prob])
      print("End of Baseline Test")

      # Reading time
      time.sleep(8) # 0:38 - 0:46

      # Expiration Test #1
      writer.writerow(['Expiration Test #1'])
      for i in range(4):
         time.sleep(15)
         phasic, tonic = gsr_model.predict()
         speech, prob = speech_model.predict()
         writer.writerow([phasic, tonic, speech, prob])
      print("End of Expiration Test")

      # Reading time
      time.sleep(10) # 1:46 - 1:56

      # Rest #1
      writer.writerow(['Rest #1'])
      stress = input("Enter stress level rating 0-5: ")
      writer.writerow([None,None,None,None,stress])
      for i in range(2):
         time.sleep(15)
         phasic, tonic = gsr_model.predict()
         speech, prob = speech_model.predict()
         writer.writerow([phasic, tonic, speech, prob, stress])
      print("End of Rest #1")

      # Reading time
      time.sleep(8) # 2:26 - 2:34

      # Expiration Test #2
      writer.writerow(['Expiration Test #2'])
      for i in range(4):
         time.sleep(15)
         phasic, tonic = gsr_model.predict()
         speech, prob = speech_model.predict()
         writer.writerow([phasic, tonic, speech, prob])
      print("End of Expiration #2 Test")

      # Reading time
      time.sleep(8) # 3:34 - 3:42

      # Rest #2
      writer.writerow(['Rest #2'])
      stress = input("Enter stress level rating 0-5: ")
      writer.writerow([None,None,None,None,stress])
      for i in range(2):
         time.sleep(15)
         phasic, tonic = gsr_model.predict()
         speech, prob = speech_model.predict()
         writer.writerow([phasic, tonic, speech, prob, stress])
      print("End of Rest #2")

      # Reading time
      time.sleep(8) # 4:12 - 4:20

      # Video Test #3
      writer.writerow(['Video Test #3'])
      for i in range(10):
         time.sleep(15)
         phasic, tonic = gsr_model.predict()
         speech, prob = speech_model.predict()
         writer.writerow([phasic, tonic, speech, prob])
      print("End of Video Test")

      # Reading time
      time.sleep(9) # 6:50 - 6:59

      # Rest #3
      writer.writerow(['Rest #3'])
      stress = input("Enter stress level rating 0-5: ")
      writer.writerow([None,None,None,stress])
      for i in range(2):
         time.sleep(15)
         phasic, tonic = gsr_model.predict()
         speech, prob = speech_model.predict()
         writer.writerow([phasic, tonic, speech, prob, stress])
      print("End of Rest #3")

      # Reading time
      time.sleep(6) # 7:29 - 7:35

      # Reciting Test #4
      writer.writerow(['Reciting Test #4'])
      for i in range(2):
         time.sleep(15)
         phasic, tonic = gsr_model.predict()
         speech, prob = speech_model.predict()
         writer.writerow([phasic, tonic, speech, prob])
      print("End of Reciting Test #4")

      # Reading time
      time.sleep(5) # 8:05 - 8:10

      # Rest #4
      writer.writerow(['Rest #4'])
      stress = input("Enter stress level rating 0-5: ")
      writer.writerow([None,None,None,None,stress])
      for i in range(2):
         time.sleep(15)
         phasic, tonic = gsr_model.predict()
         speech, prob = speech_model.predict()
         writer.writerow([phasic, tonic, speech, prob, stress])
      print("End of Rest #4")
   file.close()
   return


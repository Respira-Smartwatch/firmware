#import json
import GSRClassifier
import SpeechEmotionClassifier

class Aggregate:
	def __init__(self):
		self.gsr = GSRClassifier()
		self.speech = SpeechEmotionClassifier()

	def datafromgsr(self): 
		#reads data from eda classifier
		gsrdata = self.gsr.predict()
		gsrtonic = gsrdata[1]
		gsrphasic = gsrdata[0]

	def datafromspeech(self):
		speechdata = self.speech.predict()
	
	def combinedata(self):
		#combines data from eda and gsr

	def LED(self):
		#LED Meaning
		#All LED change hue as Phasic level increases
		#Happy:
			#LED1: on, LED2: on, LED3: on
		#Sad:
			#LED1: off, LED2: on, LED3: on
		#Discust:
			#LED1: off, LED2: off, LED3: on
		#Suprised:
			#LED1: off, LED2: on, LED3: off

threshold = 15
if (Aggregate.datafromgsr.gsrtonic() > threshold):
	#combinedata


##old
		# data = json.load(open('respira_Max_2023-02-22.json', 'r'))
		# phases = ['baseline', 'expiration1', 'rest1', 'expiration2', 'rest2', 'video', 'rest3', 'recitation', 'rest4']
		# phasic = []
		# tonic = []

		# for i in phases:
		# 	for j in data[i]['gsr_phasic']:
		# 		phasic.append(j)

	##if values reach a certain threshold, then the speech classifier is ran

		

	#values from speech classifer are read
	#values from speech and eda classifer are then outputted to the LED's on the pi
	#Useful info
		#https://static5.arrow.com/pdfs2/2019/3/24/12/39/13/69153/seeed_/manual/respeaker2-micspihat.pdf
	#Use these commands to run pixels.py
		# sudo pip install spidev
		# cd ~/
		# git clone https://github.com/respeaker/mic_hat.git
		# cd mic_hat
		# python pixels.py
	#apa102.py is driver for APA102 LEDs
		#combine_color is one rgb value that outputs one color to all three LEDs
		#set_pixel_rgb sets the color of one pixel
	#speech outputs: happy, sad, disgust, suprised



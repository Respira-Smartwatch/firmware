import GSRClassifier
import SpeechEmotionClassifier


# Get GSR Precition
# Get Speech Prediction
# Combine these in some meaningful way to guage total stress
# GSR gives instant stress *(physiological)
# Speech gives psychological stress

class Aggregate:
	def __init__(self, threshold: int=5):
		self.gsr = GSRClassifier()
		self.speech = SpeechEmotionClassifier()
		self.threshold = threshold

	def predict(self, samples):
		#average tonic and phasic to make baseline
		#compare new values to previous baseline
		#if new value - baseline is > threshold, then activate speech classifier
		#both tonic and phasic have to be > threshold

		ran = 0
		psamples = 0
		tsamples = 0
		for s in range(samples):
			phasic, tonic = self.gsr.predict()
			tsamples += tonic
			tonicbl = tonic - (tsamples / (s + 1))

			#only runs speech classifier once during sampling
			if tonic - tonicbl > self.threshold and ran == 0:
				speech_data = self.speech.predict()
				ran = 1


		
		
	
		#combine gsr and speech values
		stress_value = tonic + speech_data[0]
			
		#turn on LEDs based on new value
		self.LED(tonic, speech_data, stress_value)
		return stress_value
		

	def LED(self, gsr_stress: float, speech_stress: list, combines_value: float):
		
		# DO SOMETHING BASED ON THOSE VALUES


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
		pass



if __name__ == "__main__":
	print(Aggregate.predict(30))
	
	
	
	
	
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



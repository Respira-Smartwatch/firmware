# Author: Joseph Bellahcen <joeclb@icloud.com>

.PHONY: respeaker_drivers
respeaker_drivers:
	@echo "########################################"
	@echo "#    INSTALLING RESPEAKER DRIVERS     #"
	@echo "########################################"
	git clone https://github.com/respeaker/seeed-voicecard .seeed
	cd .seeed && sudo ./install.sh
	rm -rf .seeed

.PHONY: speech_eda_env
speech_eda_env:
	@echo "########################################"
	@echo "#   INSTALLING MODULE DEPENDENCIES    #"
	@echo "########################################"
	git submodule update --init --recursive
	$(MAKE) -C Models/speech-emotion-classifier setup
	$(MAKE) -C Models/eda-classifier setup

setup: respeaker_drivers speech_eda_env
	sudo apt install portaudio19-dev python3-pyaudio
	pip3 install -r requirements.txt


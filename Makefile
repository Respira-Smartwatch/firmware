# Author: Joseph Bellahcen <joeclb@icloud.com>

respeaker_drivers:
    git clone https://github.com/respeaker/seeed-voicecard .seeed
    sudo .seeed/install.sh
.PHONY: respeaker_drivers

speech_eda_env:
    git submodule update --init --recursive
    make -C Models/speech-emotion-classifier/Makefile setup
    make -C Models/eda-classifier/Makefile setup
.PHONY: speech_eda_env


#!/bin/bash
sudo apt install git &&
git clone https://github.com/HinTak/seeed-voicecard.git &&
sudo ./seeed-voicecard/install.sh 2mics &&
sudo reboot

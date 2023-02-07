# Respira Firmware
This repository contains the firmware for the development prototype of the
Respira Smartwatch.

## Preparing the Raspberry Pi
Assuming `git` is already installed, please ensure Python and Pip are present
on the system. Next, use the provided Makefile to install remaining depdencies.

```shell
$ sudo apt install python3-pip
$ make setup
```

## Repository Structure
### ReSpeaker\_Drivers

   This folder condtains modules for using the ReSpeaker unit

   __button.py__: implements a button class to use the button of the ReSpeaker with any `on_button_func()` desired

   __apa102.py__: is a direct copy of the apa102 led driver supplied with the respeaker firmware

   __pixels.py__: is a short file to utilize the leds on the board, and can be played with. Again, this is a direct copy

   __mics.py__: implements a Mics class that allows for both mono, and stereo recording. It is based off of the give ncode in the respeaker driver library, but allows for easy use, and quick startup. See code for documentation.


### Data\_Drivers

   This folder contains files related to data collection

   __dataflow.py__: Implements a live data collection/plotting class

   __gsr.py__:      This file implements a simple gsr class to utilize gsr via the i2c bus.
   
   __main.py__:      This is temporarily the main file which will deal with linking all drivers, using dataflow collection methods, and running the analysis

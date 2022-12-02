#firmware

A repository for firmware developed for the Raspberry Pi prototype of Respira

## Using this file
   In this file there is included a `setup` directory, which holds shell scripts for setting
   up the raspberry pi with all required modules and firmware to run the ReSpeaker hat.
   in the `ReSpeaker_Drivers` directory several python drivers have been placed to handle IO with
   the respeaker board.
   the best place to start is running the setup scripts. 
### Setup 
	
   The `setup` directory contains scripts to do important raspberry pi setup. 

   __"seeed.sh"__ : a script that will install git, and pull the seeed firmware onto the board,
                    it will install this firmware, and perform a reboot. 
                    After this is complete, run `arecord -l` and confirm that the seeed card 
		    is being detected correctly.

   __"py_setup.sh"__: a script that installs pip, and installs requirements from requirements.txt

### ReSpeaker\_Drivers

   This folder condtains modules for using the ReSpeaker unit

   __button.py__: implements a button class to use the button of the ReSpeaker with any `on_button_func()` desired

   __apa102.py__: is a direct copy of the apa102 led driver supplied with the respeaker firmware

   __pixels.py__: is a short file to utilize the leds on the board, and can be played with. Again, this is a direct copy

   __mics.py__: implements a Mics class that allows for both mono, and stereo recording. It is based off of the give ncode in the respeaker driver library, but allows for easy use, and quick startup. See code for documentation.


### Data\_Drivers

   This folder contains files related to data collection

   __dataflow.py__: Implements a live data collection/plotting class


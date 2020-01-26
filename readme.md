## NeoTrellis M4 Circuit Python Music Fun
**Requires: [adafruit_neotrellism4](https://github.com/adafruit/Adafruit_CircuitPython_TrellisM4)**

This project consists of two parts: 

The first one is the wave_generator script which needs to be run on a PC with regular python. It will create a bunch of music note .wav files. You must create a folder called `notes` on the neotrellis device and paste a copy of the wave files into it. E.g. `notes/c3.wav etc...` 

The second is the CircuitPython code.py file that will run on the neotrellis device. After you pasted your wave files into the `notes` folder you can put this `code.py` on the neotrellis. 
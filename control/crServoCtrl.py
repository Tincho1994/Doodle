#!/usr/bin/env python
import os
import sys
import struct
import time
import operator
import threading

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) # Use broadcom numbering
# Set output pins - pin 26 BCM, pin 37 BOARD
GPIO.setup(26,GPIO.OUT)

# Set frequency to 70 Hz - period=20ms
# Full Stop - High for 1.5 ms -- 7.5% duty cycle
# Full Forward - high for 2.0 ms -- 10.0% duty cycle
# Full Backward - high for 1.0 ms -- 5.0% duty cycle 
p= GPIO.PWM(26,70) # Set BCM pin 26 at 70Hz
p.start(7.5)	   # Set duty cycle to 7.5% and start

# Spin for 30 seconds
timeElapsed = time.tim()
try: 
        while time.time()-timeElapsed < 30:
                pass
        
except KeyboardInterrupt:
        GPIO.cleanup()
GPIO.cleanup()

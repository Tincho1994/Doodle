#!/usr/bin/env/python
# Authors: Diego Horna (dh468), Deepthi Krovvidi (dk562)
# Lab 3 pwm_calibrate cde
# October 2, 2017

import RPi.GPIO as GPIO         #import RPi.GPIO module
import time
import sys

def RunCal(pin):

	GPIO.setmode(GPIO.BCM)          # choose BCM
	GPIO.setup(pin, GPIO.OUT)       # set pin as an output

	pwm = GPIO.PWM(pin, 50)          # setting pin and frequency
	pwm.start(0)                    # start LED on 0% duty cycle (off)

	try:
	        while True:
	                pwm.ChangeDutyCycle(7.5)

	except KeyboardInterrupt:
	        pwm.stop()              # stop PWM output
	        GPIO.cleanup()          # cleanup GPIO on CTRL+C Exit
			return
if __name__ = '__main__':
	pin = int(sys.argv[1])
	RunCal(pin)
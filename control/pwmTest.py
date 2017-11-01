#!/usr/bin/env/python
# Authors: Martin Herrera, Deepthi Krovvidi
# Project: Doodle, 10/30/2017
# Purpose: Testing the right and left wheel servos

import RPi.GPIO as GPIO         #import RPi.GPIO module
import time
import sys
import math
import json
import speed2DC

def RunTest(rwpin, rwcenter, rwspeed, lwpin, lwcenter, lwspeed):

	GPIO.setmode(GPIO.BCM)          # choose BCM
	GPIO.setup(rwpin, GPIO.OUT)     # set pin as an output
	GPIO.setup(lwpin, GPIO.OUT)     # set pin as an output

	rpwm = GPIO.PWM(rwpin, 50)      # setting pin and frequency
	rpwm.start(0)                   # start LED on 0% duty cycle (off)
	lpwm = GPIO.PWM(lwpin, 50)      # setting pin and frequency
	lpwm.start(0)                   # start LED on 0% duty cycle (off)

	centers = {str(rwpin) : rwcenter, str(lwpin) : lwcenter}
	json.dump(centers, open("calib_servo.txt",'w'))

	rwDC = speed2DC(rwpin, rwspeed)
	lwDC = speed2DC(lwpin, lwspeed)
	print 'right wheel duty cycle: ' + str(rwDC)
	print 'left wheel duty cycle: '  + str(lwDC)

	rpwm.ChangeDutyCycle(rwDC)
	lpwm.ChangeDutyCycle(lwDC)

	time.sleep(3)

	rpwm.stop()
	lpwm.stop()
	GPIO.cleanup()
	return 

if __name__ == '__main__':
	rwpin      = int(sys.argv[1])
	rwcenter   = float(sys.argv[2])
	rwspeed    = float(sys.argv[3])
	lwpin      = int(sys.argv[4])
	lwcenter   = float(sys.argv[5])
	lwspeed    = float(sys.argv[6])
	RunTest(rwpin, rwcenter, rwspeed, lwpin, lwcenter, lwspeed)
#!/usr/bin/env/python
# Authors: Martin Herrera, Deepthi Krovvidi
# Project: Doodle, 10/30/2017
# Purpose: Testing the right and left wheel servos

#import RPi.GPIO as GPIO         #import RPi.GPIO module
import pigpio
import time
import sys
import math
import json
import speed2DC

def RunTest(duty13,duty18):

	#GPIO.setmode(GPIO.BCM)          # choose BCM
	#GPIO.setup(rwpin, GPIO.OUT)     # set pin as an output
	#GPIO.setup(lwpin, GPIO.OUT)     # set pin as an output

	#rpwm = GPIO.PWM(rwpin, 50)      # setting pin and frequency
	#rpwm.start(0)                   # start LED on 0% duty cycle (off)
	#lpwm = GPIO.PWM(lwpin, 50)      # setting pin and frequency
	#lpwm.start(0)                   # start LED on 0% duty cycle (off)

	#centers = {str(rwpin) : rwcenter, str(lwpin) : lwcenter}
	#json.dump(centers, open("calib_servo.txt",'w'))

	#rwDC = speed2DC.speed2DC(rwpin, rwspeed)
	#lwDC = speed2DC.speed2DC(lwpin, lwspeed)
	#print 'right wheel duty cycle: ' + str(rwDC)
	#print 'left wheel duty cycle: '  + str(lwDC)

	#rpwm.ChangeDutyCycle(rwDC)
	#lpwm.ChangeDutyCycle(lwDC)

	pi1 = pigpio.pi()
	pi1.hardware_PWM(13,100,int(duty13))
	pi1.hardware_PWM(18,100,int(duty18))
	time.sleep(5)
	pi1.hardware_PWM(18,100,0)
	pi1.hardware_PWM(13,100,0)
	pi1.stop()
	#rpwm.stop()
	#lpwm.stop()
	#GPIO.cleanup()
	return 

if __name__ == '__main__':
	duty13      = float(sys.argv[1])*10000
	duty18   = float(sys.argv[2])*10000
	#rwspeed    = float(sys.argv[3])
	#lwpin      = int(sys.argv[4])
	#lwcenter   = float(sys.argv[5])
	#lwspeed    = float(sys.argv[6])
	
	RunTest(duty13,duty18)

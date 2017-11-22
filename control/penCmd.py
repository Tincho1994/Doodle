#!/usr/bin/env/python
# Authors: Martin Herrera and Deepthi Krovvidi


import RPi.GPIO as GPIO         #import RPi.GPIO module
import time
import sys

def penActuation(pin, dir):
     GPIO.setmode(GPIO.BCM)          # choose BCM
     GPIO.setup(pin, GPIO.OUT)       # set pin as an output
     pwm = GPIO.PWM(pin, 50)         # setting pin and frequency
     pwm.start(0)                    # start LED on 0% duty cycle (off)

     # 0 degrees is 2.72 and 180 degrees is 12

     if dir == 'up':
     	pwm.ChangeDutyCycle(2.72)
	print 'up'
     if dir == 'down':
     	pwm.ChangeDutyCycle(12)
	print 'down'

     pwm.stop()
     GPIO.cleanup()

if __name__ == '__main__':
        pin = int(sys.argv[1])
        dir = str(sys.argv[2])
        penActuation(pin, dir)
	time.sleep(1)

#!/usr/bin/env/python
#Authors: Martin Herrera and Deepthi Krovvidi 

import RPi.GPIO as GPIO         #import RPi.GPIO module
import time
import sys

def RunCal(pin):

        GPIO.setmode(GPIO.BCM)          # choose BCM
        GPIO.setup(pin, GPIO.OUT)       # set pin as an output
        pwm = GPIO.PWM(pin, 50)         # setting pin and frequency
        pwm.start(0)                    # start LED on 0% duty cycle (off)

        try:

                while True:
			#print('Sleeping')
			#pwm.ChangeDutyCycle(2.72)
			time.sleep(2)
			print('Running')
			#pwm.ChangeDutyCycle(9)
			pwm.ChangeDutyCycle(12)
			time.sleep(1)
        except KeyboardInterrupt:
                pwm.ChangeDutyCycle(2.72)
                pwm.stop()              # stop PWM output
                GPIO.cleanup()          # cleanup GPIO on CTRL+C Exit
                return
if __name__ == '__main__':
        pin = int(sys.argv[1])
        RunCal(pin)

#!/usr/bin/env/python
# Authors: Martin Herrera, Deepthi Krovvidi
# Project: Doodle, 10/31/2017
# Purpose: To take in speed, offset for the desired center, and output duty cycle

import sys
import math
import json

def speed2DC(pin, speed):

	# Setting the variables to calculate the speed
	# These values are from Martin's MATLAB calibration code
	m = 0.0243 
        if speed < 0:
          m=-m
          speed = -speed
	b = 7.7454

	# Calculating the duty cycle
	dc = (10**speed)*m + b 

	# Offsetting for the stable duty cycle of the specific servo assigned to the pin
	center_pt = json.load(open("calib_servo.txt"))
	pin_center = str(pin)
	offset = center_pt[pin_center] - (m+b)
	dc = dc + offset

	# returning the duty cycle
	return dc

if __name__ == '__main__':
	pin   = int(sys.argv[1])
	speed = float(sys.argv[2])
	out = speed2DC(pin, speed)
	print out

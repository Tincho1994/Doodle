#!/usr/bin/env python
import os
import sys
import struct
import time
import operator
import threading

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.OUT)


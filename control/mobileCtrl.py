#!/usr/bin/env python
import bluetooth
import RPi.GPIO as GPIO 
import sys
import struct
import time
import operator
import threading
import speed2DC  
import os

class doodleBot(object):

  def __init__(self):
      self.pipe = self.connect2pipe()
      self.rwpin = 21
      self.lwpin = 20
      self.penpin = 16

  def initIO(self):
    GPIO.setmode(GPIO.BCM)               # choose BCM
    GPIO.setup(self.rwpin, GPIO.OUT)     # set pin as an output
    GPIO.setup(self.lwpin, GPIO.OUT)     # set pin as an output
    self.rPWM = GPIO.PWM(self.rwpin, 50)
    self.lPWM = GPIO.PWM(self.lwpin, 50)
    self.rPWM.start(0)
    self.lPWM.start(0)

  def connect2pipe(self):
    self.path = "/home/pi/doodle_code/comms/command.fifo"
    file_exists = os.path.exists(self.path)
    if not file_exists:
      os.mkfifo(self.path)
    return open(self.path,"r",1)

  def parseCmd(self,cmd):
    cmdParsed  = cmd.split(',')
    #print cmdParsed[0]
    if (len(cmdParsed) < 3) and (len(cmdParsed) > 0):
      finCmdL = float(cmdParsed[0])
      cmdParsed2 = cmdParsed[1].split('/')
      finCmdR = float(cmdParsed2[0])
    print([finCmdL,finCmdR])
    return [finCmdL,finCmdR]

  def changeVel(self,lVel, rVel):
    rDuty = speed2DC.speed2DC(self.rwpin, rVel)
    lDuty = speed2DC.speed2DC(self.lwpin, lVel)
    if rVel == 0:
      rDuty = 50
    if lVel == 0:
      lDuty = 50
    #print 'right wheel duty cycle: ' + str(rDuty)
    #print 'left wheel duty cycle: '  + str(lDuty)

    self.rPWM.ChangeDutyCycle(rDuty)
    self.lPWM.ChangeDutyCycle(lDuty)
  def openFifo(self):
    return open(self.path,'r',1)

  def cleanup(self):
    self.rPWM.stop()
    self.lPWM.stop()
    GPIO.cleanup()

if __name__ =='__main__':
  ctrl = doodleBot()
  fifo = ctrl.connect2pipe()
  ctrl.initIO()
  try:
    while True:
      line = fifo.readline()
      if len(line) == 0:
        print("Writer closed")
        fifo.close()
        fifo = ctrl.openFifo()
      else:
        print line
        cmd = ctrl.parseCmd(line)
        #print(cmd[0]+','+cmd[1])
        ctrl.changeVel(cmd[0],cmd[1])
  except KeyboardInterrupt:
    print("\n Keyboard Interrupt Detected Cleaning Up \n")
  ctrl.cleanup()

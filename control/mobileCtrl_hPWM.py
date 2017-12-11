#!/usr/bin/env python
import bluetooth
#import RPi.GPIO as GPIO 
import pigpio
import sys
import struct
import time
import operator
import threading
import speed2DCduo  
import os

class doodleBot(object):

  def __init__(self):
      self.pipe = self.connect2pipe()
      self.rwpin = 18
      self.lwpin = 13
      self.penpin = 16

  def initIO(self):
    self.piPWM = pigpio.pi()
    self.freq = 100
    self.piPWM.hardware_PWM(self.rwpin,self.freq,0)
    self.piPWM.hardware_PWM(self.lwpin,self.freq,0)

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
    #print([finCmdL,finCmdR])
    return [finCmdL,finCmdR]

  def changeVel(self,lVel, rVel):
    rDuty = speed2DCduo.speed2DC(self.rwpin, rVel)
    lDuty = speed2DCduo.speed2DC(self.lwpin, lVel)
    if rVel == 0:
      rDuty = 0
    if lVel == 0:
      lDuty = 0
    #print str(self.rwpin)+' wheel duty cycle: ' + str(rDuty)
    #print str(self.lwpin)+' wheel duty cycle: '  + str(lDuty)
    rDuty_adj = 10000*rDuty
    lDuty_adj = 10000*lDuty
    self.piPWM.hardware_PWM(self.rwpin,self.freq,rDuty_adj)
    self.piPWM.hardware_PWM(self.lwpin,self.freq,lDuty_adj)
  def openFifo(self):
    return open(self.path,'r',1)

  def cleanup(self):
    self.piPWM.hardware_PWM(self.rwpin,self.freq,0)
    self.piPWM.hardware_PWM(self.lwpin,self.freq,0)
    self.piPWM.stop()

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

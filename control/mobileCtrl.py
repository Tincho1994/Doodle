#!/usr/bin/env python
import bluetooth
import RPi.GPIO as GPIO 
import sys
import struct
import time
import operator
import threading
import speed2DC 

class doodleBot(object):

  def __init__(self):
      self.pipe = connect2pipe()
      self.rwpin = 26
      self.lwpin = 30

  def initIO():
    GPIO.setmode(GPIO.BCM)               # choose BCM
    GPIO.setup(self.rwpin, GPIO.OUT)     # set pin as an output
    GPIO.setup(self.lwpin, GPIO.OUT)     # set pin as an output
    self.rPWM = GPIO.PWM(self.rwpin, 50)
    self.lPWM = GPIO.PWM(self.lwpin, 50)
    self.rPWM.start(0)
    self.lPWM.start(0)

  def connect2pipe():
    path = "~/doodle_code/comms/command.fifo"
    file_exists = os.path.exists(path)
    if not file_exists:
      os.mkfifo(path)
    return open(path,"r",1)

  def parseCmd(cmd):
    cmdParsed  = cmd.split(',')
    if (len(cmdParsed) < 3) and (len(cmdParsed) > 0):
      finCmd[0] = float(cmdParsed[0])
      finCmd[1] = float(cmdParsed[1])
    else:
      finCmd = []
    return finCmd

  def changeVel(lVel, rVel):
    rDuty = speed2DC(rwpin, rwspeed)
    lDuty = speed2DC(lwpin, lwspeed)

    print 'right wheel duty cycle: ' + str(rDuty)
    print 'left wheel duty cycle: '  + str(lDuty)

    rpwm.ChangeDutyCycle(rDuty)
    lpwm.ChangeDutyCycle(lDuty)

  def cleanup():
    self.rPWM.stop()
    self.lPWM.stop()
    GPIO.cleanup()

if __name__ =='__main__':
  ctrl = doodleBot()
  fifo = ctrl.connect2pipe()

try:
  while True:
    line = fifo.readline()
    if len(line) == 0:
        print("Writer closed")
        fifo.close()
        fifo = openFifo(target_name)
    else:
      cmd = ctrl.parseCmd(line)
      print(cmd[0]+','+cmd[1])
      ctrl.changeVel(cmd[0],cmd[1])
  except KeyboardInterrupt:
    print("\n Keyboard Interrupt Detected Cleaning Up \n")
  ctrl.cleanup()
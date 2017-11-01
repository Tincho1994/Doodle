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

if __name__ =='__main__':
  ctrl = doodleBot()
  fifo = ctrl.connect2pipe()

  while True:
    line = fifo.readline()
    if len(line) == 0:
        print("Writer closed")
        fifo.close()
        fifo = openFifo(target_name)
    else:
      cmd = ctrl.parseCmd(line)
      print(cmd[0]+','+cmd[1])
#!/usr/bin/env python
import bluetooth
import sys
import struct
import time
import operator
import threading

hostMACAddress  = 'B8:27:EB:1B:BE:1B'
backlog = 1
port  = 5
size = 1024

class BTInterface_Slave(object):

  def __init__(self):
      self.target_name = ""
      self.hostMACAddress = hostMACAddress
      self.port = port
      self.size = size
      self.pipe = connect2pipe()
      self.sock = None

  def connect2pipe():
    path = "./command.fifo"
    file_exists = os.path.exists(path)
    if not file_exists:
      os.mkfifo(path)
    return open(path,"w",1)

  def listen(self):
    try:
      self.sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
      self.sock.bind((self.hostMACAddress,self.port))
      self.sock.listen(backlog)
      client, clientinfo = self.sock.accept()
      while 1:
        data = client.recv(size)
        if data:
          self.pipe.write(data + "\n")
          self.pipe.flush()
          print(data)

    except bluetooth.btcommon.BluetoothError as error:
      sys.stdout.write(str(error.strerror))
      sys.stdout.flush()
      time.sleep(5.0)
      sys.exit(1)

if __name__ =='__main__':
  listener = BTInterface_Slave()
  listener.listen()

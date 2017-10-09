#!/usr/bin/env python
import bluetooth
import sys
import struct
import time
import operator
import threading

serverMACAddress = 'B8:27EB:1B:BE:1B'
port = 1
size = 1024
class BTInterface_Master(object):

  def __init__(self):
  	  self.target_name = ""
      self.port = port
      self.device_found = False
      self.tries = 0
      self.target_addr = serverMACAddress
      self.sock = None

  def connect(self):
    # if self.target_addr is None:

    #     for i in range(10):
    #       nearby_devices = bluetooth.discover_devices(lookup_names = True)

    #       if len(nearby_devices)>0:
    #         for bdaddr, name in nearby_devices:
    #           if name.startswith(self.target_name):
    #             self.device_found = True
    #             self.target_addr = bdaddr
    #             break
    #       if self.device_found:
    #         break

    try:
      self.sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
      self.sock.connect((self.target_address,self.port))
    except bluetooth.btcommon.BluetoothError as error:
      sys.stdout.write(error.strerror)
      sys.stdout.flush()
      time.sleep(5.0)
      sys.exit(1)
    sys.stdout.write("Paired with Pi @ " + self.target_addr + "\n")
    sys.stdout.flush()
    return True

  def send(self, data):
    self.sock.send(data)

  def recv(self, num_bytes):
    return self.sock.recv(num_bytes)

  def close(self):
    self.sock.close()

if __name__ =='__main__':
  master = BTInterface_Master()
  master.send("Test test")
  master.close()
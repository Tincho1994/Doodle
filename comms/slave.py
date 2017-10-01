#!/usr/bin/env python
import bluetooth
import sys
import struct
import time
import operator
import threading

hostMACAddress  = 'B8:27:EB:1B:BE:1B'
backlog = 1
port  = 1
size = 1024

class BTInterface_Slave(object):

  def __init__(self):
      self.target_name = ""
      self.hostMACAddress = hostMACAddress
      self.port = port
      self.size = size
      self.sock = None

  def listen(self):

    if self.target_addr is None:

        for i in range(10):
          nearby_devices = bluetooth.discover_devices(lookup_names = True)

          if len(nearby_devices)>0:
            for bdaddr, name in nearby_devices:
              if name.startswith(self.target_name):
                self.device_found = True
                self.target_addr = bdaddr
                break
          if self.device_found:
            break

    try:
      self.sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
      self.sock.connect((self.hostMACAddress,self.port))
      self.sock.listen(backlog)
      client, clientinfo = self.sock.accept()
      while 1:
        data = client.recv(size)
        if data:
          print(data)

    except bluetooth.btcommon.BluetoothError as error:
      sys.stdout.write(error.strerror)
      sys.stdout.flush()
      time.sleep(5.0)
      sys.exit(1)

if __name__ =='__main__':
  listener = BTInterface_Slave()
  listener.listen()

#!/usr/bin/env python
import bluetooth
import sys
import struct
import time
import operator
import threading

#Laptop MAC A4:02:B9:4D:13:1C
serverMACAddress = 'B8:27:EB:1B:BE:1B'
port = 5
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

		# for i in range(10):
		# 	nearby_devices = bluetooth.discover_devices(lookup_names = True)

		# 	if len(nearby_devices)>0:
		# 		for bdaddr, name in nearby_devices:
		# 			print(name)
		

		try:
			self.sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
			self.sock.connect((self.target_addr,self.port))
		except bluetooth.btcommon.BluetoothError as error:
			sys.stdout.write(error.strerror)
			sys.stdout.flush()
			time.sleep(5.0)
			sys.exit(1)
		sys.stdout.write("Paired with Pi @ " + self.target_addr + "\n")
		sys.stdout.flush()
		return True

if __name__ =='__main__':
	master = BTInterface_Master()
	master.connect()
	master.sock.send("Test test")
	master.sock.close()
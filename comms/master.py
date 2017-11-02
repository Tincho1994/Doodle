#!/usr/bin/env python
import bluetooth
import cv2
import os
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
		self.connected = False
	def connect(self):
		try:
			self.sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
			self.sock.connect((self.target_addr,self.port))
		except bluetooth.btcommon.BluetoothError as error:
			#sys.stdout.write(error.strerror)
			#sys.stdout.flush()
			time.sleep(1.0)
			#sys.exit(1)
			print('reattemptng pairing')
		sys.stdout.write("Paired with Pi @ " + self.target_addr + "\n")
		sys.stdout.flush()
		master.connected = True
		return True

	def openFifo(self):
		path = "./bluetooth.fifo"
		file_exists = os.path.exists(path)
		if not file_exists:
			os.mkfifo(path)
		return open(path,"r",0)

if __name__ =='__main__':
	master = BTInterface_Master()
	#while(~master.connected):
	master.connect()
	print('Connected')
	fifo = master.openFifo()
	while(True):
		line = fifo.readline()
		# ------------------------------------------------------------
		# If writer side of fifo is finished, close fifo and reopen it
		# so that a new program can send commands
		# ------------------------------------------------------------
		if len(line) == 0:
			print("Writer closed")
			fifo.close()
			fifo = master.openFifo()
		# ----------------------------------------------------------------
		# Else, writer has written a line of commands parse the commands
		# as numbers and have sphero object send via BT
		# ----------------------------------------------------------------
		else:
			master.sock.send(line)
			print('Line Detected')
			print(line)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	master.sock.close()

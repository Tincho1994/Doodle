#!/usr/bin/env/python
import sys
import os
import struct

path = './bluetooth.fifo'
fifo = open(path,'r',1)
while(True):
	line = fifo.readline()
	if len(line)==0:
		print("writer closed")
		fifo.close()
		fifo = open(path,'r',1)
	else:
		print(line)

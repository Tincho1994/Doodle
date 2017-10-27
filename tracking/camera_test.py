#!/usr/bin/env/python
import numpy as np
import cv2
import picamera
import picamera.array

#cap = cv2.VideoCapture(0)
camera = picamera.PiCamera()
stream = picamera.array.PiRGBArray(camera)
camera.resolution = (640,480)
#camera.framerate = 32
while(True):
	camera.capture(stream, 'bgr', use_video_port=True)
	#ret, frame = cap.read()
	#frame = stream.array
	#gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	cv2.imshow('frame',stream.array)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	stream.seek(0)
	stream.truncate()

cap.release()
cv2.destroyAllWindows

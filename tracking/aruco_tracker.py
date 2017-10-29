#!/usr/bin/env python
import numpy as np
import math
import cv2
import cv2.aruco as aruco
import picamera
import picamera.array 
 
#cap = cv2.VideoCapture(0)
camera = picamera.PiCamera()
stream = picamera.array.PiRGBArray(camera)

camera.framerate = 60
camera.resolution = (640,480)
print(cv2.__version__)
while(True):
    # Capture frame-by-frame
    #ret, frame = cap.read()
    camera.capture(stream, 'bgr', use_video_port=True)
    frame = stream.array
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
 

    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    if corners:  
      #print(corners[0][0][0])
    
      fL = corners[0][0][0]
      fR = corners[0][0][1]
      bR = corners[0][0][2]
      cP = [(fL[0]+bR[0])/2, (fL[1]+bR[1])/2]
      tP = [(fL[0]+fR[0])/2,(fL[1]+fR[1])/2]
      ang = math.atan2(cP[1]-tP[1],tP[0]-cP[0])*180/math.pi
      print(ang)
    #It's working.
    # my problem was that the cellphone put black all around it. The alrogithm
    # depends very much upon finding rectangular black blobs
 
      gray = aruco.drawDetectedMarkers(frame, corners)
      gray = cv2.circle(gray,(corners[0][0][0][0],corners[0][0][0][1]),10,(0,0,255),-1)
      gray = cv2.circle(gray,(corners[0][0][2][0],corners[0][0][2][1]),10,(255,0,0),-1)
      gray = cv2.circle(gray,(int(cP[0]),int(cP[1])),10,(0,255,0),-1)
      gray = cv2.circle(gray,(int(tP[0]),int(tP[1])),10,(0,255,255),-1)
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    stream.seek(0)
    stream.truncate() 
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

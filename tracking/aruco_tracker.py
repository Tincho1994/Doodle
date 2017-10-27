#!/usr/bin/env python
import numpy as np
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
    print(corners)
 
    #It's working.
    # my problem was that the cellphone put black all around it. The alrogithm
    # depends very much upon finding rectangular black blobs
 
    gray = aruco.drawDetectedMarkers(gray, corners)

    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    stream.seek(0)
    stream.truncate() 
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

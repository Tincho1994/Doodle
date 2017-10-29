#!/usr/bin/env/python
import numpy as np
import cv2
import cv2.aruco as aruco
import picamera
import picamera.array 

with np.load('calib.npz') as X:
	mtx,dist,rvecs,tvecs=[X[i] for i in ('mtx','dist','rvecs','tvecs')]

camera = picamera.PiCamera()
stream = picamera.array.PiRGBArray(camera)
w = 640
h = 480
camera.framerate = 60
camera.resolution = (w,h)
camera.capture(stream, 'bgr', use_video_port=True)
frame = stream.array
h,w = frame.shape[:2]
newcameramtx, roi =cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
x,y,w1,h1 = roi
stream.seek(0)
stream.truncate() 
while(True):
    # Capture frame-by-frame
    #ret, frame = cap.read()
    camera.capture(stream, 'bgr', use_video_port=True)
    frame = stream.array
    new_frame = cv2.undistort(frame,mtx,dist,None,newcameramtx)
    new_frame = new_frame[y:y+h1, x:x+w1]
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    new_gray = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
 

    new_corners, new_ids, rejectedImgPoints = aruco.detectMarkers(new_gray, aruco_dict, parameters=parameters)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

 
    #It's working.
    # my problem was that the cellphone put black all around it. The alrogithm
    # depends very much upon finding rectangular black blobs
 
    gray = aruco.drawDetectedMarkers(gray, corners)
    new_gray = aruco.drawDetectedMarkers(new_gray, new_corners)

    cv2.imshow('frame',gray)
    cv2.imshow('new_frame',new_gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    stream.seek(0)
    stream.truncate() 

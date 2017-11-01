#!/usr/bin/env python
import numpy as np
import math
import cv2
import cv2.aruco as aruco
import picamera
import picamera.array 
 
def calcVec(pose,dest):
  if pose:
    vec = [[dest[0]-pose[0]],[pose[1]-dest[1]]]
    velVec = vec/(np.linalg.norm(vec))
  else:
    velVec =[]
  return velVec

def linVel(pose,vel):
    ang = math.radians(pose[2])
    epsilon = float(2)
    R = [[math.cos(ang),math.sin(ang)],[-math.sin(ang),math.cos(ang)]]
    T = np.dot([[1,0],[0,1/epsilon]],R)
    vLin = np.dot(T,vel)
    
    return vLin
#cap = cv2.VideoCapture(0)
camera = picamera.PiCamera()
stream = picamera.array.PiRGBArray(camera)

camera.framerate = 60
camera.resolution = (640,480)

destVec = [[320,240]]
curDestInd = 0
curDest = destVec[0]
curPose = []

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
 
      #gray = aruco.drawDetectedMarkers(frame, corners)
      frame = cv2.circle(gray,(int(cP[0]),int(cP[1])),10,(0,255,0),-1)
      curPose = [cP[0],cP[1], ang]
    frame = cv2.circle(frame,(int(curDest[0]),int(curDest[1])),10,(255,0,0),-1)
    cv2.imshow('frame',frame)
    velVec = calcVec(curPose,curDest)
    velLin = linVel(curPose,velVec)
    print(velLin)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    stream.seek(0)
    stream.truncate() 
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
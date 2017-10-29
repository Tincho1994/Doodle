#!/usr/bin/env python
import numpy as np
import sys
import cv2
import glob

# termination criteria
numRow = 9
numCol = 6
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((numCol*numRow,3), np.float32)
objp[:,:2] = np.mgrid[0:numRow,0:numCol].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('*.jpg')
print images
for fname in images:
    print fname
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imshow('img',img)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (numRow,numCol),None)
    print ret
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        #img = cv2.drawChessboardCorners(img, (numRow,numCol), corners2,ret)
        #cv2.imshow('img',img)
        #cv2.waitKey(0)

ret,mtx,dist,rvecs,tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
print mtx
calibFile = open('calib.npz','w')
np.savez(calibFile, ret=ret,mtx=mtx,dist=dist,rvecs=rvecs,tvecs=tvecs)
cv2.destroyAllWindows()

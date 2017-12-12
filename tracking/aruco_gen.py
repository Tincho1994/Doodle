#!/usr/bin/env python
import numpy as np
import cv2
import cv2.aruco as aruco
 
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
print(aruco_dict)
# second parameter is id number
# last parameter is total image size
img = aruco.drawMarker(aruco_dict, 3, 700)
cv2.imwrite("test_marker_3.jpg", img)
 
cv2.imshow('frame',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

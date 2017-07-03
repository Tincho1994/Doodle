# Code adapted from "4 Point OpenCV getPerspective Transform Example"
# by Adrian Rosebrock on pyimagesearch.com
#
# Martin Herrera

import numpy as np
import cv2

def order_points(pts):
	#initialize list of coordinates corresponding to top-
	#left, top-right, bottom-left, and bottom-right in order
	rect = np.zeros((4,2), dtype= "float32")
	
	#top-left has largest sum, bottom-right the smallest
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)] 
	
	diff = np.diff(pts,axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]

	#return the ordered coordinates
	return rect

def four_point_transform(image, pts):
        #obtain a consistent order of the points and unpack
        rect = order_points(pts)
        (tl, tr, bl, br) = rect

        # Compute width of new image
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] -tl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        maxWidth = max(int(widthA),int(widthB))

        # Compute height of new image
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA),int(heightB))

        # Create destination array for mapping of image
        dst = np.array([
                [0,0],
                [maxWidth-1,0],
                [maxHeight-1, 0],
                [maxHeight-1, maxWidth-1]], dtype = "float32")

        # Compute perspective transform matrix
        M = cv2.getPerspectiveTransform(rect,dst)

        # Apply perspective transform matrix
        warped = cv2.warpPerspective(image,M,(maxWidth,maxHeight))

        # return warped image
        return warped
        
        
                         

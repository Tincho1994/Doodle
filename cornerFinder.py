from vision import transform
from skimage.filters import threshold_adaptive
import numpy as np
import argparse
import cv2

def resizeIm(image,height):
	r = height / image.shape[1]
	dim = (height , int(image.shape[0] * r))
	return cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

howHeight = 600
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to the image to be scanned")
args = vars(ap.parse_args())

# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
image = cv2.imread(args["image"])
ratio = image.shape[0] / 500.0
orig = image.copy()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)
edged2 = np.float32(edged)
dst = cv2.cornerHarris(edged2,2,3,0.04)
#dst = cv2.dilate(dst,None)

#image[dst>0.05*dst.max()]=[0,0,255]

print (dst.shape)
(height, width) = dst.shape

lTx = width-1
lTy = height-1

rTx = 0
rTy = height -1

lBx = width - 1
lBy = 0

rBx = 0
rBy = 0

max = dst.max()
for x in range(0,width-1):
	for y in range(0,height-1):
		if (dst[y,x]  > 0.05*max):
			if (x+y < lTx+lTy):
				lTx = x
				lTy = y
			if (x+y > rBx+rBy):
				rBx = x
				rBy = y
			if (y-x < rTy-rTx):
				rTx = x
				rTy = y
			if (x-y < lBx-lBy):
				lBx = x
				lBy = y

L=[[lTx,lTy],[rTx,rTy],[rBx,rBy],[lBx,lBy]]
ctr = np.array(L).reshape((-1,1,2)).astype(np.int32)
cv2.drawContours(image,[ctr],0,(0,255,0),2)

cv2.imshow('dst',image)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()
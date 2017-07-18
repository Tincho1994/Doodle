# import the necessary packages
from vision import transform
from skimage.filters import threshold_adaptive
import numpy as np
import argparse
import cv2

def resizeIm(image,height):
	r = height / image.shape[1]
	dim = (height , int(image.shape[0] * r))
	return cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

showHeight = 600
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
#image = imutils.resize(image, height = 500)

# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)

# show the original image and the edge detected image
print ("STEP 1: Edge Detection")
cv2.imshow("Image", resizeIm(image,showHeight))
cv2.imshow("Edged", resizeIm(edged,showHeight))
cv2.waitKey(0)
cv2.destroyAllWindows()

# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
(_,cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

# loop over the contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)

	# if our approximated contour has four points, then we
	# can assume that we have found our screen
	if len(approx) > 4:
		screenCnt = approx
		break

# show the contour (outline) of the piece of paper
print ("STEP 2: Find contours of paper")
cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
cv2.imshow("Outline", resizeIm(image,showHeight))
cv2.waitKey(0)
cv2.destroyAllWindows()

# apply the four point transform to obtain a top-down
# view of the original image
warped = transform(orig, screenCnt.reshape(4, 2) * ratio)

# convert the warped image to grayscale, then threshold it
# to give it that 'black and white' paper effect
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
warped = threshold_adaptive(warped, 251, offset = 10)
warped = warped.astype("uint8") * 255

# show the original and scanned images
print ("STEP 3: Apply perspective transform")
cv2.imshow("Original",resizeIm(orig,showHeight))
cv2.imshow("Scanned", resizeIm(warped,showHeight))
cv2.waitKey(0)
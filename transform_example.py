# import the necessary packages
from vision.transform import four_point_transform
import numpy as np
import argparse
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i","--image", help = "path to the image file")
ap.add_argument("-c","--coords", help = "comma seperated l;ist of points")
args = vars(ap.parse_args())

# load image and grab the source coordinates\
image = cv2.imread(args["image"])
pts = np.array(eval(args["coords"]), dtype = "float32")

# apply four point transform
warped  = four_point_transform(image, pts)

# show the original and warped images
cv2.imshow("Original", image)
cv2.imshow("Warped",warped)
cv2.waitKey(0)


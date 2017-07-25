from __future__ import division
import numpy as np
import cv2
import json

def rotate(image, angle, center = None, scale = 1.0):
    (h, w) = image.shape[:2]

    if center is None:
        center = (w / 2, h / 2)

    # Perform the rotation
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))

    return rotated


def detectCircles(img):

	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY )
	img = cv2.medianBlur(img, 5)
	cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

	circles = cv2.HoughCircles(img, cv2.cv.CV_HOUGH_GRADIENT, 1, 20,
							   param1=50, param2=25, minRadius=0, maxRadius=50)



	if (circles is None):
		return img,0

	circles = np.uint16(np.around(circles))
	for i in circles[0, :]:
		# draw the outer circle
		cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
		# draw the center of the circle
		cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)

	return cimg, circles


def detectTriangles(img):

	height, width = img.shape[:2]
	response = {"triangles": [], "img_width": int(width) , "img_height": int(height) }

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)

	#ret, thresh = cv2.threshold(blurred,127,255,cv2.THRESH_BINARY)
	thresh = cv2.adaptiveThreshold(blurred,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)


	contours, h = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

	counter = 0

	for cnt in contours:

		approx = cv2.approxPolyDP(cnt,0.2*cv2.arcLength(cnt,True),True)
		area = cv2.contourArea(cnt)

		if len(approx) == 3:

			m = cv2.moments(cnt)
			cx = int(m["m10"] / m["m00"])
			cy = int(m["m01"] / m["m00"])

			cv2.circle(img, (cx, cy), 7, (255, 255, 255), -1)
			cv2.drawContours(img,[cnt],-1,(0,255,0),2)

			response["triangles"].append({"x": cx, "y": cy, "size": area, "x_ratio": cx/width, "y_ratio": cy/height})
			counter += 1

	response["total"] = counter

	return img, thresh, response

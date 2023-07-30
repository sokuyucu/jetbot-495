# import the necessary packages
import numpy as np
import imutils
import cv2

import time

color_ranges = {
    'orange': ((5, 100, 150), (15, 255, 255), (0, 140, 255)),
    'red': ((0, 100, 150), (10, 255, 255), (0, 0, 255)),
    'green': ((40, 100, 100), (80, 255, 255), (0, 255, 0)),
}

width, height = 800, 600
boundry_x1, boundry_y1 = 0, 0
boundry_x2, boundry_y2 = 200, 400
line_thickness = 2

class SingleMotionDetector:
	def __init__(self, accumWeight=0.5):
		# store the accumulated weight factor
		self.accumWeight = accumWeight
		# initialize the background model
		self.bg = None

	def update(self, image):
		# if the background model is None, initialize it
		if self.bg is None:
			self.bg = image.copy().astype("float")
			return
		# update the background model by accumulating the weighted
		# average
		cv2.accumulateWeighted(image, self.bg, self.accumWeight)

	def detect(self, image, tVal=25):
		# compute the absolute difference between the background model
		# and the image passed in, then threshold the delta image
		delta = cv2.absdiff(self.bg.astype("uint8"), image)
		thresh = cv2.threshold(delta, tVal, 255, cv2.THRESH_BINARY)[1]
		# perform a series of erosions and dilations to remove small
		# blobs
		thresh = cv2.erode(thresh, None, iterations=2)
		thresh = cv2.dilate(thresh, None, iterations=2)

		# find contours in the thresholded image and initialize the
		# minimum and maximum bounding box regions for motion
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		(minX, minY) = (np.inf, np.inf)
		(maxX, maxY) = (-np.inf, -np.inf)

		# if no contours were found, return None
		if len(cnts) == 0:
			return None
		# otherwise, loop over the contours
		for c in cnts:
			# compute the bounding box of the contour and use it to
			# update the minimum and maximum bounding box regions
			(x, y, w, h) = cv2.boundingRect(c)
			(minX, minY) = (min(minX, x), min(minY, y))
			(maxX, maxY) = (max(maxX, x + w), max(maxY, y + h))
		# otherwise, return a tuple of the thresholded image along
		# with bounding box
		return (thresh, (minX, minY, maxX, maxY))

    
    
    
# DETECT COLOUR
	def detectColour(self, image):
		detected=False
		start_time = time.time()
		frame_count = 0

		lower_black = np.array([0, 0, 0])
		upper_black = np.array([180, 255, 70])
        

		black_cup_list_area=list()
		black_cup_nparray=np.empty((0,4),dtype=int)
        
        # Blur out the noise
		kernel2 = np.ones((15, 15), np.float32)/225
		image = cv2.filter2D(src=image, ddepth=-1, kernel=kernel2)
        
		# Convert the image to grayscale
		gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		# Calculate FPS
 
		hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		frame_count += 1
		elapsed_time = time.time() - start_time
		fps = frame_count / elapsed_time

		# Create a mask for black regions based on contour area
		black_mask = cv2.inRange(hsv_image, lower_black, upper_black)
		black_contours, _ = cv2.findContours(black_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		# Iterate through the color ranges
		for color, (lower, upper, rectangle_color) in color_ranges.items():
			# Create a mask based on the color range
			mask = cv2.inRange(hsv_image, np.array(lower), np.array(upper))

			# Apply morphological operations to remove noise
			kernel = np.ones((15, 15), np.uint8)
			mask = cv2.erode(mask, kernel, iterations=5)
			mask = cv2.dilate(mask, kernel, iterations=5)

			# Find contours of the detected objects
			contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

			# Iterate through the contours and draw bounding rectangles around the objects
			for contour in contours:
				x, y, w, h = cv2.boundingRect(contour)
				cv2.rectangle(image, (x, y), (x + w, y + h), rectangle_color, 2)

		# Draw bounding rectangles for black regions
		for contour in black_contours:
			area = cv2.contourArea(contour)
			if area > 50:  # Set a suitable area threshold to filter out small black regions
				x, y, w, h = cv2.boundingRect(contour)
				cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), 2)
				black_cup_list_area.append(w*h)
				nparray=np.array([x,y,w,h])
				black_cup_nparray=np.append(black_cup_nparray,[nparray],axis=0)



		# Display the original image with bounding rectangles
		detected_offset = 20000
		detected_center_x = 20000
		detected_size_x = 20000
		if (len(black_cup_list_area))>0:    
			index_of_black_cup=black_cup_list_area.index(max(black_cup_list_area))
			detected=True
			#print(index_of_black_cup)
			#print(black_cup_nparray)
			#print(black_cup_nparray[index_of_black_cup])  # x y w h
			#print(image.shape)
			#print(detected)		
            
			detected_center_x = black_cup_nparray[index_of_black_cup][0] + black_cup_nparray[index_of_black_cup][2]/2
			detected_offset = 960-detected_center_x
            detected_size_x = black_cup_nparray[index_of_black_cup][2]

        
        #centering boundries
		height = image.shape[0]
		width = image.shape[1]
		cv2.line(image, (int(width/4), 0), (int(width/4), height), (0, 0, 0), thickness=line_thickness)
		cv2.line(image, (width-int(width/4), 0), (width-int(width/4), height), (0, 0, 0), thickness=line_thickness)
		return (image,detected,detected_offset,detected_size_x)

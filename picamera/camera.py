from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (480, 320)
camera.framerate = 30
camera.hflip = True

rawCapture = PiRGBArray(camera, size=(480, 320))
 
# allow the camera to warmup
time.sleep(0.1)
 
def nothing(x):
	pass

img = np.zeros((300,512,3),np.uint8)
cv2.namedWindow('HSV Calibration')

cv2.createTrackbar('H','HSV Calibration',0,179,nothing)
cv2.createTrackbar('S','HSV Calibration',0,255,nothing)
cv2.createTrackbar('V','HSV Calibration',0,255,nothing)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array

        #blur = cv2.blur(image, (3,3))

        #hsv to complicate things, or stick with BGR
        hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        #thresh = cv2.inRange(hsv,np.array((0, 200, 200)), np.array((20, 255, 255)))

	h = cv2.getTrackbarPos('H','HSV Calibration')
	s = cv2.getTrackbarPos('S','HSV Calibration')
	v = cv2.getTrackbarPos('V','HSV Calibration')

        lower = np.array([h,s,v],dtype="uint8")
        upper = np.array([179,255,255], dtype="uint8")
	
        mask = cv2.inRange(hsv, lower, upper)
	output = cv2.bitwise_and(image, image, mask=mask)

        #thresh = cv2.inRange(blur, lower, upper)
        #thresh2 = thresh.copy()

        # find contours in the threshold image
        #image, contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

        # finding contour with maximum area and store it as best_cnt
        #max_area = 0
        #best_cnt = 1
        #for cnt in contours:
        #        area = cv2.contourArea(cnt)
        #        if area > max_area:
        #                max_area = area
        #                best_cnt = cnt

        # finding centroids of best_cnt and draw a circle there
        #M = cv2.moments(best_cnt)
        #cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        #if best_cnt>1:
        #cv2.circle(blur,(cx,cy),10,(0,0,255),-1)
        # show the frame
        #cv2.imshow("Frame", blur)
        cv2.imshow('PiCamera',np.hstack([image, output]))
        key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
        rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
        if key == ord("q"):
        	break

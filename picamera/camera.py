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

cv2.createTrackbar('Hmin','HSV Calibration',0,179,nothing)
cv2.createTrackbar('Hmax','HSV Calibration',0,179,nothing)
cv2.createTrackbar('Smin','HSV Calibration',0,255,nothing)
cv2.createTrackbar('Smax','HSV Calibration',0,255,nothing)
cv2.createTrackbar('Vmin','HSV Calibration',0,255,nothing)
cv2.createTrackbar('Vmax','HSV Calibration',0,255,nothing)


circular_val = np.zeros([360, 105, 2])

for angle in range(0, 360):
                angle_rad = angle*np.pi/180
                for i in range(0, 105):
                        circular_val[angle, i, 0] = 105 + i*np.sin(angle_rad);
                        circular_val[angle, i, 1] = 105 + i*np.cos(angle_rad);

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array

        #blur = cv2.blur(image, (3,3))

        #hsv to complicate things, or stick with BGR
        hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        #thresh = cv2.inRange(hsv,np.array((0, 200, 200)), np.array((20, 255, 255)))

	hmin = cv2.getTrackbarPos('Hmin','HSV Calibration')
	smin = cv2.getTrackbarPos('Smin','HSV Calibration')
	vmin = cv2.getTrackbarPos('Vmin','HSV Calibration')

	hmax = cv2.getTrackbarPos('Hmax','HSV Calibration')
	smax = cv2.getTrackbarPos('Smax','HSV Calibration')
	vmax = cv2.getTrackbarPos('Vmax','HSV Calibration')

        lower = np.array([hmin,smin,vmin],dtype="uint8")
        upper = np.array([hmax,smax,vmax], dtype="uint8")
        
        mask = cv2.inRange(hsv, lower, upper)
	output = cv2.bitwise_and(image, image, mask=mask)

	cropped_img = image[50:260, 115:325]
	cropped_output = output[50:260, 115:325]
        
        #summed_output = np.zeros([360,3])
        #for angle in range(0, 360):
        #        for i in range(0, 105):
        #                summed_output[angle] += cropped_output[circular_val[angle, i, 0], circular_val[angle, i, 1]]
                        #summed_output[angle] += cropped_output[0, 0]
                        #cropped_output[105 + i*np.sin(angle), 105 + i*np.cos(angle)] = (255, 0, 255)
                        #cropped_output[105 + i*np.sin(angle) + 1, 105 + i*np.cos(angle) + 1] = (255, 0, 255)
                        #cropped_output[105 + i*np.sin(angle) - 1, 105 + i*np.cos(angle) - 1] = (255, 0, 255)
        

        params = cv2.SimpleBlobDetector_Params()
        #params.filterByCircularity = True
        #params.minCircularity = 0.1
        params.filterByArea = True
        params.minArea = 100
        params.minDistBetweenBlobs = 10

        #Inversion of value channel in hsv because blob detector looks for black blobs
        val_inv = np.invert(cropped_output[:,:,2])
        
        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(val_inv)
        im_k = cv2.drawKeypoints(val_inv, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.imshow("Points", im_k)

        for keypoint in keypoints:
                print "x: " + str(keypoint.pt[0])
                print "y: " + str(keypoint.pt[1])
                #print angle using center of circle
                #subtract 90 degrees to make forward 0 degrees
                print "angle: " + str(np.arctan2(keypoint.pt[1]-105,keypoint.pt[0]-105)*180/np.pi-90)


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
        #cv2.imshow('PiCamera',np.hstack([image, output]))
        cv2.imshow('PiCamera Cropped',np.hstack([cropped_img, cropped_output]))
        key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
        rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
        if key == ord("q"):
        	break

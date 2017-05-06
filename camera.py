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
 
img = np.zeros((300,512,3),np.uint8)

circular_val = np.zeros([360, 105, 2])

for angle in range(0, 360):
                angle_rad = angle*np.pi/180
                for i in range(0, 105):
                        circular_val[angle, i, 0] = 105 + i*np.sin(angle_rad);
                        circular_val[angle, i, 1] = 105 + i*np.cos(angle_rad);

params = cv2.SimpleBlobDetector_Params()
params.minThreshold = 0
params.maxThreshold = 255
params.minDistBetweenBlobs = 20

params.filterByCircularity = True
params.minCircularity = 0
params.maxCircularity = 1

params.filterByArea = True
params.minArea = 10

params.filterByConvexity = True
params.minConvexity = 0
params.maxConvexity = 1

params.filterByInertia = True
params.minInertiaRatio = 0
params.maxInertiaRatio = 1

params.minDistBetweenBlobs = 10
params.filterByColor = True
params.blobColor = 255

detector = cv2.SimpleBlobDetector_create(params)

counter = 0
lights = 0

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array

        hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

        lower = np.array([92,37,164],dtype="uint8")
        upper = np.array([110,198,255], dtype="uint8")
        
        mask = cv2.inRange(hsv, lower, upper)
        output = cv2.bitwise_and(image, image, mask=mask)

	cropped_img = image[50:260, 115:325]
        cropped_output = output[50:260, 115:325]
        cropped_hue = np.copy(cropped_output[:,:,0])
        cropped_sat = np.copy(cropped_output[:,:,1])
        cropped_val = np.copy(cropped_output[:,:,2])
        cropped_gray = cv2.addWeighted(cropped_hue, 0.5, cropped_sat, 0.5, 0.0)
        cropped_gray[cropped_gray > 0] = 255


        keypoints = detector.detect(cropped_gray)
        #im_k = cv2.drawKeypoints(cropped_gray, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

	if counter == 10:
		print "I see " + str(lights/10.) + " lights."
		counter = 0
		lights = 0
	lights += len(keypoints)
	counter += 1
	
        #for keypoint in keypoints:
                #print "x: " + str(keypoint.pt[0])
                #print "y: " + str(keypoint.pt[1])
                #print angle using center of circle
                #subtract 90 degrees to make forward 0 degrees
                #angle = np.arctan2(keypoint.pt[1]-105,keypoint.pt[0]-105)*180/np.pi-90
                #if(angle < -180):
                #        angle += 360
                #print "angle: " + str(angle) + " size: " + str(keypoint.size)

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
 

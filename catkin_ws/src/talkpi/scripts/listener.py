#!/usr/bin/env python

from __future__ import print_function

import roslib
roslib.load_manifest('talkpi')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np

def callback(data):
    try:
        bridge = CvBridge()
        #detector = cv2.SimpleBlobDetector_create()
        cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        print(e)

    #(rows,cols,channels) = cv_image.shape
    #if cols > 60 and rows > 60 :
    #    cv2.circle(cv_image, (50,50), 10, 255)

    #cv_image_edge = cv2.Canny(cv_image,100,200)
    #keypoints = detector.detect(cv_image)
    #cv_image_keys = cv2.drawKeypoints(cv_image, keypoints,
    #        np.array([]),(0,0,255))

    cv2.imshow("Image window", cv_image)
    cv2.waitKey(100)

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("image_topic",Image,callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()

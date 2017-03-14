#!/usr/bin/python

import rospy
from geometry_msgs.msg import Twist

import serial

ser=serial.Serial('/dev/ttyACM0',115200)

going_fwd = False
turning_left = False
turning_right = False

def callback(data):
	global going_fwd
	global turning_left
	global turning_right
	if ( data.linear.x > 3.5 and not going_fwd ):
		ser.write(bytearray(['D',0x00,0x00,0x00,0x00,100,'E']))
		going_fwd = True
		turning_left = False
		turning_right = False
		print "forward"
	elif ( data.angular.z > 3.5 and not turning_right ):
		ser.write(bytearray(['D',100,100,0,0,100,'E']))
		going_fwd = False
		turning_left = False
		turning_right = True
		print "right"
	elif ( data.angular.z < -3.5 and not turning_left):
		ser.write(bytearray(['D',0,0,100,100,100,'E']))
		going_fwd = False
		turning_left = True
		turning_right = False
		print "left"
	elif ( not ( data.linear.x > 3.5 ) and not ( data.angular.z > 3.5 ) and not ( data.angular.z < -3.5 ) and ( going_fwd or turning_left or turning_right ) ):
		ser.write(bytearray(['D',0x00,0x00,0x00,0x00,0x00,'E']))
		going_fwd = False
		turning_left = False
		turning_right = False
		print "nothing"

def listener():

	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber("/cmd_vel", Twist, callback)

	rospy.spin()

if __name__ == '__main__':
	listener()

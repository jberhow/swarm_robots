#!/usr/bin/python

import rospy
from geometry_msgs.msg import Twist

import serial

ser=serial.Serial('/dev/ttyACM0',115200)

def callback(data):

	if ( data.linear.x > 3.5 ):
		ser.write(bytearray(['D',0x00,0x00,0x00,0x00,100,'E']))
	elif ( data.angular.z > 3.5 ):
		ser.write(bytearray(['D',100,100,0,0,100,'E']))
	elif ( data.angular.z < -3.5 ):
		ser.write(bytearray(['D',0,0,100,100,100,'E']))
	else:
		ser.write(bytearray(['D',0x00,0x00,0x00,0x00,0x00,'E']))

def listener():

	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber("/cmd_vel", Twist, callback)

	rospy.spin()

if __name__ == '__main__':
	listener()

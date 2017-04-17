#!/usr/bin/python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

def callback(data):
    twist = Twist()
    twist.linear.x = 4*data.axes[1]
    twist.angular.z = 4*data.axes[0]
    #twist.angular.x = 4*data.axes[3]
    #twist.angular.y = 4*data.axes[4]
    pub.publish(twist)

def start():
    global pub
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    rospy.Subscriber("joy", Joy, callback)
    rospy.init_node('controller')
    rospy.spin()

if __name__ == '__main__':
    start()

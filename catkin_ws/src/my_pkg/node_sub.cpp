#include "ros/ros.h"
#include "std_msgs/String.h"

void helloCallback(const std_msgs::String::ConstPtr& msg) // passed in a shared pointer (boostlib)
{
  ROS_INFO("I heard: [%s]", msg->data.c_str()); // example response
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "node_sub");

  ros::NodeHandle n; // needed to communicate with others

  // connects to master node and sends messages to topic_name via cb function
  ros::Subscriber sub = n.subscribe("hello", 1000, helloCallback);

  // this keeps calling the cb function forever, or until killed (no need for
  // loop in this case)
  ros::spin();

  return 0;
}

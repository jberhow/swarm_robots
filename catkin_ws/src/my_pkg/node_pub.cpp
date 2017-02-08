#include "ros/ros.h"
#include "std_msgs/String.h"

int main(int argc, char **argv)
{
  ros::init(argc, argv, "speaker");

  ros::NodeHandle n; // needed to communicate with node

  // connects to master node with topic name and returns publisher
  ros::Publisher hello_pub = n.advertise<std_msgs::String>("hello", 1000);

  ros::Rate loop_rate(10);

  int count = 0; // count the messages
  while (ros::ok())
  {
    std_msgs::String msg; // create a message type
    
    msg.data = "Hello!";

    ROS_INFO("%s", msg.data.c_str());

    hello_pub.publish(msg);

    ros::spinOnce();

    loop_rate.sleep();
    ++count;
  }


  return 0;
}

#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry

rospy.init_node('fuse_odom', anonymous=True)

class FuseOdom:

    def __init__(self):

        # Define subscribers
        self.z_sub = rospy.Subscriber("/z_state_estimator/odom", Odometry, self.zStateEstimatorCallback)
        self.xy_sub = rospy.Subscriber("/tf_odom", Odometry, self.cartographerCallback)

        # Define publishers
        self.pub = rospy.Publisher('fused_odom', Odometry, queue_size=10)

        # Create messages
        self.fused_odom_msg = Odometry()
       
        while not rospy.is_shutdown():
            rospy.spin()

    def zStateEstimatorCallback(self, msg):
   
        self.fused_odom_msg.pose.pose.position.z = msg.pose.pose.position.z
        self.fused_odom_msg.twist.twist.linear.z = msg.twist.twist.linear.z

    def cartographerCallback(self, msg):

        self.fused_odom_msg.pose.pose.position.x = msg.pose.pose.position.x
        self.fused_odom_msg.pose.pose.position.y = msg.pose.pose.position.y
        self.fused_odom_msg.pose.pose.orientation.z = msg.pose.pose.orientation.z
        self.fused_odom_msg.pose.pose.orientation.w = msg.pose.pose.orientation.w

        self.fused_odom_msg.header.stamp = rospy.Time.now()
        self.fused_odom_msg.header.frame_id = 'world'
        self.pub.publish(self.fused_odom_msg)

    def fused_odom_publisher(fused_odom):

        # In ROS, nodes are uniquely named. If two nodes with the same
        # name are launched, the previous one is kicked off. The
        # anonymous=True flag means that rospy will choose a unique
        # name for our 'listener' node so that multiple listeners can
        # run simultaneously.

        self.fused_odom_msg.header.stamp = rospy.Time.now()
        rospy.loginfo(self.fused_odom_msg)
        pub.publish(self.fused_odom_msg)

if __name__ == '__main__':
    try:
        FuseOdom()
    except rospy.ROSInterruptException:
        pass


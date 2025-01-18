#!/usr/bin/env python3

import rospy
from visualization_msgs.msg import Marker,MarkerArray
from std_msgs.msg import Header
from geometry_msgs.msg import Point
from std_msgs.msg import Float32MultiArray
from functools import partial

# Callback function to handle incoming data
class Rviz_marker_node:
    def __init__(self):
        rospy.init_node("marker_visualizer", anonymous=False)
        self.markers=[]
        self.id_counter=0
        # Create a publisher to the `visualization_marker` topic
        self.marker_pub = rospy.Publisher("visualization_marker_array", MarkerArray, queue_size=10)

        # Subscribe to the topic you want to read data from
        rospy.Subscriber("predicted_gaps", Float32MultiArray, lambda msg: self.topic_callback(msg, "extra_argument"))

        

    def topic_callback(self,msg,extra_arg):
        # Create a marker
        marker = Marker()
        print(extra_arg)
        # Set the frame ID and timestamp
        marker.header = Header()
        marker.header.frame_id = "map"  # Change this to the relevant frame
        marker.header.stamp = rospy.Time.now()

        # Set the namespace and id for the marker
        marker.ns = "example_namespace"
        marker.id = self.id_counter

        # Set the type of marker (e.g., SPHERE, LINE_STRIP, etc.)
        marker.type = Marker.CYLINDER  # Change to Marker.LINE_STRIP or others if needed

        # Set the action for the marker (add, modify, delete)
        marker.action = Marker.ADD

        # Set the pose of the marker
        marker.pose.position.x = msg.data[0]  # Assume `data` has attributes x, y, z
        marker.pose.position.y = 0
        marker.pose.position.z = 0
        marker.pose.orientation.x = 0.0
        marker.pose.orientation.y = 0.0
        marker.pose.orientation.z = 0.0
        marker.pose.orientation.w = 1.0

        # Set the scale of the marker
        marker.scale.x = 0.2  # Scale along the x-axis
        marker.scale.y = 0.2  # Scale along the y-axis
        marker.scale.z = 2# Scale along the z-axis

        # Set the color (RGBA)
        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0
        marker.color.a = 1.0  # Transparency (1.0 is fully opaque)

        # Set the lifetime of the marker (0 means forever)
        marker.lifetime = rospy.Duration(0)

        # Publish the marker
        print("hello")
        
        self.markers.append(marker)
        self.id_counter+=1
        marker_array = MarkerArray()
        marker_array.markers = self.markers

        self.marker_pub.publish(marker_array)

    def run(self):
        # Keep the node running
        rospy.spin()

if __name__ == "__main__":
    # Initialize the ROS node
    try:
        # Create the node object
        node = Rviz_marker_node()
        # Run the node
        node.run()
    except rospy.ROSInterruptException:
        rospy.loginfo("Node terminated.")
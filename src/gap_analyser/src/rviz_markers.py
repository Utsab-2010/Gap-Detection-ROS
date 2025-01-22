#!/usr/bin/env python3

import rospy
from visualization_msgs.msg import Marker,MarkerArray
from std_msgs.msg import Header
from geometry_msgs.msg import Point
from std_msgs.msg import Float32MultiArray
# from functools import partial

# Callback function to handle incoming data
class Rviz_marker_node:
    def __init__(self):
        rospy.init_node("marker_visualizer", anonymous=False)
        self.time = (rospy.Time.now().secs + rospy.Time.now().nsecs/1e9)
        
        # self.markers=[[[],[],[]],
        #               [[],[],[]],
        #               [[],[],[]],
        #               [[],[],[]]]
        self.marker_array = MarkerArray()

        self.id_counter=[0,0,0,0]
        # Create a publisher to the `visualization_marker` topic
        self.marker_pub = rospy.Publisher("visualization_marker_array", MarkerArray, queue_size=20)

        # Subscribe to the topic you want to read data from
        rospy.Subscriber("gap_prediction/predicted_gaps_cv_model", Float32MultiArray, lambda msg: self.topic_callback(msg, "cv_model_gaps",0))
        rospy.Subscriber("gap_prediction/predicted_gaps_ca_model", Float32MultiArray, lambda msg: self.topic_callback(msg, "cv_model_gaps",1))
        rospy.Subscriber("gap_prediction/real_gaps", Float32MultiArray, lambda msg: self.topic_callback(msg, "real_gaps",2))
        rospy.Subscriber("gap_prediction/lidar_gaps", Float32MultiArray, lambda msg: self.topic_callback(msg, "lidar_gaps",3))
        # rospy.Subscriber("gap_prediction/real_gaps",Float32MultiArray,self.test_callback)

    # def test_callback(self,msg):
    #     print("hello")

    def create_marker(self,msg,namespace,sub_idx,idx):
        # Create a marker
        marker = Marker()
        # Set the frame ID and timestamp
        marker.header = Header()
        marker.header.frame_id = "map"  # Change this to the relevant frame
        marker.header.stamp = rospy.Time.now()
        print(namespace)
        # Set the namespace and id for the marker
        extra =""
        if sub_idx==0:
            extra = "/gap_12"
        elif sub_idx==1:
            extra = "/gap_23"
        elif sub_idx==2:
            extra = "/gap_31"

        marker.ns = namespace + extra
        marker.id = self.id_counter[idx]

        # Set the type of marker (e.g., SPHERE, LINE_STRIP, etc.)
        marker.type = Marker.CYLINDER  # Change to Marker.LINE_STRIP or others if needed

        # Set the action for the marker (add, modify, delete)
        marker.action = Marker.ADD

        # Set the pose of the marker
        marker.pose.position.x = -5+(msg.data[-1]-self.time)*3 # Assume `data` has attributes x, y, z
        marker.pose.position.y = 5-idx*3 -sub_idx
        marker.pose.position.z = 0
        marker.pose.orientation.x = 0.0
        marker.pose.orientation.y = 0.0
        marker.pose.orientation.z = 0.0
        marker.pose.orientation.w = 1.0

        # Set the scale of the marker
        marker.scale.x = 0.1  # Scale along the x-axis
        marker.scale.y = 0.1  # Scale along the y-axis
        marker.scale.z = msg.data[sub_idx]*0.3# Scale along the z-axis

        # Set the color (RGBA)
        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0
        marker.color.a = 1.0  # Transparency (1.0 is fully opaque)

        # Set the lifetime of the marker (0 means forever)
        marker.lifetime = rospy.Duration(0)

        # Publish the marker
        print("hello")
        
        self.marker_array.markers.append(marker)    
        # self.id_counter[idx]+=1/
        # marker_array = MarkerArray()
        # marker_array.markers.append()
        print(self.marker_array)
        self.marker_pub.publish(self.marker_array)


    def topic_callback(self,msg,namespace,idx):
        print('hi')
        self.create_marker(msg,namespace,0,idx)
        self.create_marker(msg,namespace,1,idx)
        self.create_marker(msg,namespace,2,idx)
        self.id_counter[idx]+=1

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
#!/usr/bin/env python3

import rospy
from gazebo_msgs.msg import ModelStates
from std_msgs import Float32MultiArray
from sensor_msgs import LaserScan

class Gap_Computation_Node:
    def __init__(self):
        rospy.init_node('gap_predictor_node')

        self.state_sub = rospy.Subscriber('/gazebo/model_states',ModelStates,self.model_state_callback())
        self.lidar_sub = rospy.Subscriber('/scan',LaserScan,self.lidar_callback())

        self.pub = rospy.Publisher('predicted_gaps',Float32MultiArray)

        self.real_gap=0
        self.cv_model_gap=0
        self.ca_model_gap=0

        self.cylinder_radius=0.1


    def model_state_callback(self,msg):
    #getting actual position of the obstacles
        pos = [0,0,0,0]
        for i, name in (msg.name):
            if name == "cylinder_1":  # Replace with your model's name
                # Extract position (x, y, z) of the model
                pos[0] = msg.pose[i].position.x
                pos[1] = msg.pose[i].position.y
            if name == "cylinder_2":
                pos[2] = msg.pose[i].position.x
                pos[3] = msg.pose[i].position.y

        self.real_gap = ((pos[0]-pos[2])**2 + (pos[1]-pos[3])**2)**0.5

    def lidar_callback(self,msg):
        min_1 = msg.range_max
        min_2 = min_1
        i_1 = 0
        i_2 = 0
        for i,value in enumerate(msg.ranges):
            if value <min:
                min_2,i_2 = min_1 , i_1
                min_1,i_1 = value,i
            elif value < min_2 and value!=min_1:
                min_2 , i_2 = value , i
        
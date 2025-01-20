#!/usr/bin/env python3

import rospy
from gazebo_msgs.msg import ModelStates
from std_msgs.msg import Float32MultiArray
from sensor_msgs.msg import LaserScan
import math
import numpy as np
import random   
# from dbscan_clustering2 import Lidar_Pos
from kmeans_clustering import Lidar_Pos
from gap_finder import Lidar_gaps
from prediction_models import velocity_model,acceleration_model

def get_gap(pos_1,pos_2):
    return ((pos_1[0] - pos_2[0])**2+(pos_1[1]-pos_2[1])**2)**0.5



class Gap_Computation_Node:
    def __init__(self):
        rospy.init_node('gap_predictor_node')

        self.time_step =0.2

        self.state_sub = rospy.Subscriber('/gazebo/model_states',ModelStates,self.state_sub_callback)
        self.latest_state_msg=None
        self.lidar_sub = rospy.Subscriber('/scan',LaserScan,self.lidar_sub_callback)
        self.latest_lidar_msg=None
        self.pub = rospy.Publisher('predicted_gaps',Float32MultiArray,queue_size=10)
        # print("11")
        self.timer = rospy.Timer(rospy.Duration(self.time_step), self.process_message) #0.1 s per iteration
        # print("1333")
        self.real_gap=None
        self.cv_model_gap=None
        self.ca_model_gap=None

        self.cylinder_radius=0.1
        self.pos_list = []
    
    def euclidean_distance(self,point1, point2):
        """Calculate Euclidean distance between two points."""
        return np.sqrt(np.sum((point1 - point2) ** 2))
    
    def state_sub_callback(self,msg):
        self.latest_state_msg = msg
    
    def lidar_sub_callback(self,msg):
        self.latest_lidar_msg = msg
        # print(self.latest_lidar_msg)

    def real_gap_finder(self,msg):
    #getting actual position of the obstacles
        pos = [(),(),()]
        for i, name in enumerate(msg.name):
            if name == "cylinder_1":  # Replace with your model's name
                # Extract position (x, y, z) of the model
                pos[0] = np.array([msg.pose[i].position.x,msg.pose[i].position.y])
            if name == "cylinder_2":
                pos[1] = np.array([msg.pose[i].position.x,msg.pose[i].position.y])
            if name == "cylinder_3":
                pos[2] = np.array([msg.pose[i].position.x,msg.pose[i].position.y])   


        self.real_gap = np.array([self.euclidean_distance(pos[0],pos[1]),
                                  self.euclidean_distance(pos[1],pos[2]),
                                  self.euclidean_distance(pos[2],pos[0])]) - 2*self.cylinder_radius
        
        print(f"Real coordinates: {pos[0],pos[1],pos[2]}")
        print("Real Gaps:",self.real_gap)
    
    def lidar_callback(self,msg):
        time = (rospy.Time.now().secs + rospy.Time.now().nsecs/1e9)
        N=5
        gap_object = Lidar_gaps(msg.ranges,self.cylinder_radius)
        # edge_grps = func.arrange_data()
        print("Gaps from Lidar:",gap_object.gaps)

        pos_object = Lidar_Pos(msg.ranges,self.cylinder_radius)

        pos_estimates = pos_object.pos_estimate(3)
        pos_estimates.append(time)

        self.pos_list.append(pos_estimates)
        if len(self.pos_list)>N+3:
            self.pos_list.pop(0)
            print(velocity_model(self.pos_list,self.time_step,N))
            print(acceleration_model(self.pos_list,self.time_step,N))

        print("Predicted Coordinates:",pos_estimates)

    def process_message(self,event):
        msg= Float32MultiArray()
        self.real_gap_finder(self.latest_state_msg)
        # try:
        self.lidar_callback(self.latest_lidar_msg)
        
        i = random.randint(0,20)
        msg.data = [1.1+i, 2.2, 3.3]
        self.pub.publish(msg)
        print("XX=====================================XX")
    
        
    def run(self):
        
        rospy.spin()

    
if __name__ == '__main__':
    try:
        # Create the node object
        node = Gap_Computation_Node()
        # Run the node
        node.run()
    except rospy.ROSInterruptException:
        rospy.loginfo("Node terminated.")
#!/usr/bin/env python3

import rospy
from gazebo_msgs.msg import ModelStates
from std_msgs.msg import Float32MultiArray
from sensor_msgs.msg import LaserScan
import math
import numpy 
# from dbscan_clustering2 import Lidar_Pos
from kmeans_clustering import Lidar_Pos

def get_gap(pos_1,pos_2):
    return ((pos_1[0] - pos_2[0])**2+(pos_1[1]-pos_2[1])**2)**0.5



class Gap_Computation_Node:
    def __init__(self):
        rospy.init_node('gap_predictor_node')

        self.state_sub = rospy.Subscriber('/gazebo/model_states',ModelStates,self.state_sub_callback)
        self.latest_state_msg=None
        self.lidar_sub = rospy.Subscriber('/scan',LaserScan,self.lidar_sub_callback)
        self.latest_lidar_msg=None
        self.pub = rospy.Publisher('predicted_gaps',Float32MultiArray,queue_size=10)
        # print("11")
        self.timer = rospy.Timer(rospy.Duration(0.5), self.process_message) #0.1 s per iteration
        # print("1333")
        self.real_gap=None
        self.cv_model_gap=None
        self.ca_model_gap=None

        self.cylinder_radius=0.1
        self.pos_list = []
    
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
                pos[0] = (msg.pose[i].position.x,msg.pose[i].position.y)
            if name == "cylinder_2":
                pos[1] = (msg.pose[i].position.x,msg.pose[i].position.y)
            if name == "cylinder_3":
                pos[2] = (msg.pose[i].position.x,msg.pose[i].position.y)   


        self.real_gap = (get_gap(pos[0],pos[1]),
                         get_gap(pos[1],pos[2]),
                         get_gap(pos[2],pos[0]))
        
        print(f"Real coordinates: {pos[0],pos[1],pos[2]}")

    
    def lidar_callback(self,msg):

        func = Lidar_Pos(msg.ranges,self.cylinder_radius)
        pos_estimates = func.pos_estimate(3)
        pos_estimates = sorted(pos_estimates, key=lambda point: (point[0]**2 + point[1]**2)**0.5, reverse=True)
        print("Predicted Coordinates:",pos_estimates)
        return pos_estimates
    def process_message(self,event):
        
        self.real_gap_finder(self.latest_state_msg)
        try:
            pos_estimates = self.lidar_callback(self.latest_lidar_msg)
        except:
            pass
        # self.pos_list.append(self.real)
    
        
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
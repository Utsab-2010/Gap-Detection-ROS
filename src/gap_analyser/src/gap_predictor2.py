#!/usr/bin/env python3

import rospy
from gazebo_msgs.msg import ModelStates
from std_msgs.msg import Float32MultiArray
from sensor_msgs.msg import LaserScan
import math

def get_gap(pos_1,pos_2):
    return ((pos_1[0] - pos_2[0])**2+(pos_1[1]-pos_2[1])**2)**0.5



class Gap_Computation_Node:
    def __init__(self):
        rospy.init_node('gap_predictor_node')

        self.state_sub = rospy.Subscriber('/gazebo/model_states',ModelStates,self.state_sub_callback)
        self.latest_state_msg=None
        self.lidar_sub = rospy.Subscriber('/scan',LaserScan,self.lidar_sub_callback)
        self.latest_lidar_msg=None
        self.pub = rospy.Publisher('predicted_gaps',Float32MultiArray)

        self.timer = rospy.Timer(rospy.Duration(0.1), self.process_message) #0.1 s per iteration

        self.real_gap=0
        self.cv_model_gap=0
        self.ca_model_gap=0

        self.cylinder_radius=0.1
        self.pos_list = []
    
    def state_sub_callback(self,msg):
        self.latest_state_msg = msg
    
    def lidar_sub_callback(self,msg):
        self.latest_lidar_msg = msg

    def real_gaps(self,msg):
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
        
        # print(f"1st Pos: {pos[0],pos[1]}",f"2st Pos: {pos[2],pos[3]}")

    def lidar_callback(self,msg):
        point_cloud= []
        for i,value in enumerate(msg.ranges):
            if value < 100:
                point_cloud.append((value*math.cos(i*3.14/360),value*math.sin(i*3.14/360)))

        pos_1 = ((min_1+self.cylinder_radius)*math.cos(i_1*3.14/360),(min_1+self.cylinder_radius)*math.sin(i_1*3.14/360))
        pos_2 = ((min_2+self.cylinder_radius)*math.cos(i_2*3.14/360),(min_2+self.cylinder_radius)*math.sin(i_2*3.14/360))
        
        sim_time = rospy.Time.now()

        self.pos_list.append((pos_1,pos_2,pos_3,sim_time))
        if len(self.pos_list >5):
            self.pos_list.pop(0)

    def process_message(self):
        
        self.real_gap(self.latest_state_msg)

    
        
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
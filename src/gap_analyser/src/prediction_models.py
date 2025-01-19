import math 
import numpy as np

def velocity_model(pos_list,time_step):
    del_t = pos_list[-1][-1]- pos_list[-2][-1]
    vel_1 = ((pos_list[-1][0][0]-pos_list[-2][0][0])/del_t , (pos_list[-1][0][1]-pos_list[-2][0][1])/del_t )
    vel_2 = ((pos_list[-1][1][0]-pos_list[-2][1][0])/del_t , (pos_list[-1][1][1]-pos_list[-2][1][1])/del_t )
    vel_3 = ((pos_list[-1][2][0]-pos_list[-2][2][0])/del_t , (pos_list[-1][2][1]-pos_list[-2][2][1])/del_t )


    del_p1 = time_step*np.array(vel_1)
    del_p2 = time_step*np.array(vel_2)
    del_p3 = time_step*np.array(vel_3)

    return (del_p1,del_p2,del_p3)

def acceleration_model(pos_list,time_step):
    del_t1 = pos_list[-1][-1]- pos_list[-2][-1]
    vel_11 = ((pos_list[-1][0][0]-pos_list[-2][0][0])/del_t1 , (pos_list[-1][0][1]-pos_list[-2][0][1])/del_t1 )
    vel_12 = ((pos_list[-1][1][0]-pos_list[-2][1][0])/del_t1 , (pos_list[-1][1][1]-pos_list[-2][1][1])/del_t1 )
    vel_13 = ((pos_list[-1][2][0]-pos_list[-2][2][0])/del_t1 , (pos_list[-1][2][1]-pos_list[-2][2][1])/del_t1 )

    del_t2 = pos_list[-2][-1]- pos_list[-3][-1]
    vel_21 = ((pos_list[-2][0][0]-pos_list[-3][0][0])/del_t2 , (pos_list[-2][0][1]-pos_list[-3][0][1])/del_t2 )
    vel_22 = ((pos_list[-2][1][0]-pos_list[-3][1][0])/del_t2 , (pos_list[-2][1][1]-pos_list[-3][1][1])/del_t2 )
    vel_23 = ((pos_list[-2][2][0]-pos_list[-3][2][0])/del_t2 , (pos_list[-2][2][1]-pos_list[-3][2][1])/del_t2 )

    acc_1 = (np.array(vel_11)-np.array(vel_21))/((del_t1+del_t2)/2)
    acc_2 = (np.array(vel_12)-np.array(vel_22))/((del_t1+del_t2)/2)
    acc_3 = (np.array(vel_13)-np.array(vel_23))/((del_t1+del_t2)/2)
    
    del_p1 = time_step*np.array(vel_11) + 0.5*np.array(acc_1)*time_step**2
    del_p2 = time_step*np.array(vel_12) + 0.5*np.array(acc_2)*time_step**2
    del_p3 = time_step*np.array(vel_13) + 0.5*np.array(acc_3)*time_step**2

    return (del_p1,del_p2,del_p3)
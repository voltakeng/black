#!/usr/bin/env python 

import rospy 
import cv2 
import numpy as np 
from sensor_msgs.msg import Image 
from geometry_msgs.msg import Twist 
from move_robot import MoveKobuki 
from cv_bridge import CvBridge, CvBridgeError 
from pid_control import PID 

class PID_Movement(object):
    def __init__(self):
        self.image_sub = rospy.Subscriber('/camere/rgb/image_raw', Image, self.camera_callback)
        self.bridge_object = CvBridge() 
        self.move_robot_object = MoveKobuki() 

        setPoint_value = 0.0 
        state_value = 0.0 
        self.pid_object = PID(setPoint_value, state_value) 

    def camera_callback(self, data):
        try:
            cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding='bgr8')
        except CvBridgeError as e:
            print(e) 
    
        height, width, channels = cv_image.shape 
        descentre = 160 
        rows_to_watch = 20 
        crop_image = cv_image[(height)/(2+descentre):(height)/(2+descentre+rows_to_watch)] 

        hsv = cv2.cvtColor(crop_image, cv2.COLOR_BGR2HSV) 

        upper_colour = np.array([20, 100, 100])
        lower_colour = np.array([50, 255, 255])
        mask = cv2.inRange(hsv, lower_colour, upper_colour) 

        m = cv2.moments(mask, False) 
        try:
            cx, cy = m['10']/m['00'], m['01']/m['00'] 
        except ZeroDivisionError:
            cx, cy = height/2, width/2 

        res = cv2.bitwise_and(crop_image, crop_image, mask=mask) 

        cv2.circle(res, (cx,cy), 10, (0,0,255), -1) 
        cv2.imshow('RES', res) 
        cv2.waitKey(1) 
    
        setPoint_value = width/2 
        self.pid_object.setpoint_update(setPoint_value) 

        twist_object = Twist() 
        twist_object.linear.x = 0.1 

        state_value = cx 
        self.pid_object.state_update(state_value) 

        effort_value = self.pid_object.get_control_effort() 
        rospy.logwarn('Setpoint Value => ' +str(setPoint_value))
        rospy.logwanr('State Value => ' +str(state_value)) 
        rospy.logwarn('Effort Value => ' +str(effort_value)) 

        twist_object.angular.z = effort_value/1000
        self.move_robot_object.move_robot(twist_object) 
        rospy.logwarn('Twist => ' +str(twist_object.angular.z)) 

    def clean_up(self):
        self.move_robot_object.clean_class() 
        cv2.destroyAllWIndows() 
    
def main() 
    rospy.init_node('PID_movement')
    pid_movement_object = PID_Movement()

    rate
    ctrl_c =  False 
    def shutdownhook(): 
        rospy.loginfo('Shutdown time!')
        ctrl_c  = True 
    
    rospy.on_shutdown(shutdownhook) 
    
if __name__ == '__main__': 
    main() 

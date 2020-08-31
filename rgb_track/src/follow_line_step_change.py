#!/usr/bin/env python 

import rospy
import cv2
import numpy as np 
from cv_bridge import CvBridge, CvBridgeError 
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from move_robot import MoveBlack

class LineFollower(object):
    def __init__(self):
        self.image_sub = rospy.Subscriber('/usb_cam/image_raw', Image, self.camera_callback)
        self.move_robot_object = MoveBlack()
        self.bridge_object = CvBridge() 

    def camera_callback(self, data):
        try:
            cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
        except CvBridgeError as e:
            print(e)
        
        #crop_image
        height, width, channels = cv_image.shape
        descentre = 160
        rows_to_watch = 20 
        crop_image = cv_image[(height)/(2+descentre):(height)/2+(descentre+rows_to_watch)][1:width] #[x1,x2][y1,y2]
        
        #cvt_rgb_to_hsv
        hsv = cv2.cvtColor(crop_image, cv2.COLOR_BGR2HSV)
        
        #define_colour_in_hsv
        """
        >>> yellow = np.unit8([[[B, G, R]]])
        >>> hsv_yellow = cv2.cvtColor(yellow,cv2.COLOR_BGR2HSV)
        >>> print( hsv_ yellow )
        [[[34 255 255]]]
        """

        #green: lower_colour = np.array([0,50,50]), upper_colour = np.array([255,255,255]) 
        #blue: lower_colour = np.array([33,254,254]), upper_colour = np.array([36,255,255])
        #yellow: lower_colour = np.array([20,100,100]), upper_colour = np.array([50,255,255])
        lower_colour = np.array([0,0,240])
        upper_colour = np.array([0,0,255])

        #keep only selected color 
        mask = cv2.inRange(hsv, lower_colour, upper_colour)

        #calculate centroid
        m = cv2.moments(mask, False) 
        try:
            cx, cy = m['m10']/m['m00'], m['m01']/m['m00']
        except ZeroDivisionError:
            cx, cy = height/2, width/2

        #AND operation
        res = cv2.bitwise_and(crop_image, crop_image, mask=mask)

        #Draw the centroid in the image
        #cv2.circle(img, center, radius, color, thickness)
        cv2.circle(res, (int(cx),int(cy)), 10, (0,255,255), -1)

        cv2.imshow('RES', res) 
        cv2.waitKey(10)

        #before_PID
        error_x = cx - width/2
        twist_object = Twist()
        twist_object.angular.z = -error_x/100
        twist_object.linear.x = 0.05
        rospy.loginfo('Angular Value Sent ' + str(twist_object.angular.z))
        
        self.move_robot_object.move_robot(twist_object)      

    def clean_up(self):
        self.move_robot_object.clean_class() 
        cv2.destroyAllWindows() 

def main():
    rospy.init_node('line_following_node', anonymous=True)
    line_follower_object = LineFollower()

    rate = rospy.Rate(5) 
    ctrl_c = False
    def shutdownhook():
        line_follower_object.clean_up()
        rospy.loginfo("shutdown time!")
        ctrl_c = True
    
    rospy.on_shutdown(shutdownhook)

    while not ctrl_c:
        rate.sleep()

if __name__ == '__main__':
    main()

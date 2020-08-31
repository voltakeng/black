#!/usr/bin/env python 

import rospy
import numpy as np 
import cv2 
from cv_bridge import CvBridge, CvBridgeError 
from sensor_msgs.msg import Image 
from geometry_msgs.msg import Twist 
from move_robot import MoveKobuki

class MutiCentroid(object):
    def __init__(self):
        self.image_sub = rospy.Subscriber('/camera/rgb/image_raw', Image, self.camera_callback)
        self.bridge_object = CvBridge() 
        self.move_robot_object = MoveKobuki() 
        
    def camera_callback(self, data):
        try:
            image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding='bgr8')
        except CvBridgeError as e:
            print(e) 
        
        height, width, channels = image.shape
        descentre = 160
        rows_to_watch = 20 
        crop_image = image[(height)/2+descentre:(height)/(2+descentre+rows_to_watch)][1:width]

        hsv = cv2.cvtColor(crop_image, cv2.COLOR_BGR2HSV)

        lower_colour = np.array([20,100,100])        
        upper_colour = np.array([50,255,255])

        mask = cv2.inRange(hsv, lower_colour, upper_colour)

        m = cv2.moments(mask, False)
        try:
            cx, cy = m['10']/m['00'], m['01']/m['m00']
        except ZeroDivisionError:
            cx, cy = height/2, width/2
        
        res = cv2.bitwise_and(crop_image, crop_image, mask=mask)

        contours, _, ___ = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
        rospy.loginfo("Number of centroids==>"+str(len(contours)))
        centres = []
        for i in range(len(contours)):
            moments = cv2.moments(contours[i])
            try:
                centres.append((int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00'])))
                cv2.circle(res, centres[-1], 10, (0, 255, 0), -1)
            except ZeroDivisionError:
                pass
        
        rospy.loginfo(str(centres))

        cv2.circle(res, (int(cx),int(cy)), 10, ([0,0,255]), -1)

        cv2.imshow('RES', res) 

        cv2.waitKey(10)

        error_x = cx - width/2
        twist_object = Twist() 
        twist_object.angular.z = -error_x/100
        twist_object.linear.x = 0.1
        rospy.loginfo('ANGULAR VALUE SENT ' +str(twits_object.angular.z))
        self.move_robot_object.move_robot(twist_object)

        def
def main():

            

if __main__ == '__main__':
    main()
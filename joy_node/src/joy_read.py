#!/usr/bin/env python 

from sensor_msgs.msg import Joy 
import rospy 

class JoyRead(object): 
	def __init__(self):
		rospy.loginfo('4')
		self.joy_sub = rospy.Subscriber('/joy', Joy, self.joy_callback) 
		rospy.loginfo('5')

	def joy_callback(self, data):
		rospy.loginfo('6')
		rospy.loginfo('axes is => ' +str(data.axes))
		rospy.loginfo('buttons is => ' +str(data.buttons))

def main():
	rospy.init_node('joy_read', anonymous=True)
	rospy.loginfo('2')
	joy_read_object = JoyRead()
	rospy.loginfo('3')
	rate = rospy.Rate(5)

	ctrl_c = False 
	def shutdownhook():
		ctrl_c = True 
		rospy.loginfo('Shutdown Time!')
	
	rospy.loginfo('7')
	rospy.on_shutdown(shutdownhook) 

	while not ctrl_c:
		rate.sleep()

if __name__ == '__main__': 
	rospy.loginfo('1')
	main()

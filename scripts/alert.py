#!/usr/bin/env python
import rospy, copy
from time import sleep
from pimouse_ros.msg import LightSensorValues
from std_msgs.msg import UInt16

class Alert():
    def __init__(self):
        self.alert = rospy.Publisher('/buzzer',UInt16,queue_size=1)

        self.sensor_values = LightSensorValues()
        rospy.Subscriber('/lightsensors', LightSensorValues, self.callback)

    def callback(self,messages):
        self.sensor_values = messages

    def sound(self):
        rate = rospy.Rate(10)

        buz = UInt16()
        buz = 0
        while not rospy.is_shutdown():
	    if  self.sensor_values.sum_forward >= 50:
		while True:
		    buz = 0
		    self.alert.publish(buz)
		    sleep(0.05)
		    buz = 1200
		    self.alert.publish(buz)
		    sleep(0.05)
		    if self.sensor_values.sum_forward >= 200:	break
		    elif self.sensor_values.sum_forward < 50: 	break
                while self.sensor_values.sum_all >= 200:
		    buz = 1200
		    self.alert.publish(buz)

                buz = 0
                self.alert.publish(buz)
                rate.sleep()

if __name__ == '__main__':
    rospy.init_node('alert')
    Alert().sound()

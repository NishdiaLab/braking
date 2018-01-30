#!/usr/bin/env python
import rospy, copy
from time import sleep
from std_msgs.msg import UInt16
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerResponse
from pimouse_ros.msg import LightSensorValues

class Braking():
    def __init__(self):
	self.cmd_vel = rospy.Publisher('/cmd_vel',Twist,queue_size=1)
	self.alert = rospy.Publisher('/buzzer',UInt16,queue_size=1)

	self.sensor_values = LightSensorValues()
	rospy.Subscriber('/lightsensors', LightSensorValues, self.callback)

    def callback(self,messages):
	self.sensor_values = messages

    def run(self):
	rate = rospy.Rate(10)
        data = Twist()
	buz = UInt16()

	buz = 0
        accel = 0.02
        brake = -0.12
        data.linear.x = 0.00
        while not rospy.is_shutdown():
	    data.linear.x += accel

	    if self.sensor_values.sum_all >= 50:
		data.linear.x += brake
		if data.linear.x <= 0.10:
		    data.linear.x = 0.10
		    if self.sensor_values.sum_all >= 300:	data.linear.x = 0.00
            elif data.linear.x <= 0.20:             data.linear.x = 0.20
            elif data.linear.x >= 0.80:             data.linear.x = 0.80

	    self.cmd_vel.publish(data)
	    rate.sleep()

if __name__ == '__main__':
    b = Braking()
    rospy.init_node('brake')
    rospy.wait_for_service('/motor_on')
    rospy.wait_for_service('/motor_off')
    rospy.on_shutdown(rospy.ServiceProxy('/motor_off',Trigger).call)
    rospy.ServiceProxy('/motor_on',Trigger).call()
    b.run()

#!/usr/bin/env python
import time

import rospy
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import Imu

# have to pass zero values before anything else because crazyflie firmware behaves like it is joystick-driven and doesn't want an immediate start value

class Drone(object):
    hz = 50
    move = 'takeoff'
    key = ''
    
    hover = 43000
    
    takeoff_start = 0
    
    def __init__(self):
        self.talker()

    def talker(self):
        rospy.init_node('talker', anonymous = True)
        
        rospy.loginfo("Creating cmd_vel Publisher ...")
        pub = rospy.Publisher('/crazyflie/cmd_vel', Twist, queue_size = 1)
        
        rospy.loginfo("Creating IMU Subscriber ...")
        rospy.Subscriber('/crazyflie/imu', Imu, self.imu_listener)
        
        r = rospy.Rate(self.hz)
        
        counter = 0
        while not rospy.is_shutdown():
            if(counter <= self.hz * .5):
                twist = Twist()
                counter += 1
            else:   
                twist = self.get_move()
            pub.publish(twist)
            r.sleep()     
        
    def imu_listener(self, imu):
        self.linear_acceleration = imu.linear_acceleration
        self.angular_velocity = imu.angular_velocity
        
    def get_move(self):
        thrust = self.hover
        roll = 0
        pitch = 0
        yaw = 0
    
        if(self.move == 'takeoff'):
            if(not self.takeoff_start):
                rospy.loginfo("Taking off ...")
                self.takeoff_start = time.time()
            
            thrust = (time.time() - self.takeoff_start) * 20000
            
            if(thrust > 65000):
                self.move = 'hover'
            
        elif(self.move == 'hover'):
            x = self.linear_acceleration.x
            y = self.linear_acceleration.y
            
            # x and y values move from -10 to 10, with 0 being level           
            roll = y * 2 * -1
            pitch = x * 2
            rospy.loginfo(x)
            
        # pitch (+ forward, - backward)
        # roll (+ right, - left)
        # thrust (10000 - 60000)
        # yaw  (+ clockwise, - counterclockwise)
        return Twist(Vector3(pitch, roll, thrust), Vector3(0, 0, yaw))
        
if(__name__ == '__main__'):
    Drone()

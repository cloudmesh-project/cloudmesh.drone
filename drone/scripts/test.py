#!/usr/bin/env python
# license removed for brevity
import rospy
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3

# Twist format:
# Twist(linear vector, angular vector)
# Twist((velX, velY, velZ), (roll, pitch, yaw))

def talker():
    pub = rospy.Publisher('/crazyflie/cmd_vel', Twist, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        #hello_str = {'linear': {'x': 0.0, 'y': 0.0, 'z': 30000}, 'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}}
        #rospy.loginfo(hello_str)
        pub.publish(Twist(Vector3(0, 0, 10000), Vector3(0, 0, 0)))
        rate.sleep()
        
def listener():
    sub = rospy.Subscriber('', Imu)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

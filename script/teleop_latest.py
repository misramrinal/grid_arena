#!/usr/bin/env python3
from pynput.keyboard import KeyCode,Key,Listener
import rospy
from geometry_msgs.msg import Twist

twist = Twist()


class Main:
    def __init__(self):
        self.pub = rospy.Publisher('grid_robot/cmd_vel',Twist, queue_size=10)
        rospy.init_node('teleop_py',anonymous=True)
        self.rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            
            main = self.main()
            
            
    
    def on_press(self,key):
        try:
            print('Alphanumeric key pressed: {0} '.format(
                key.char))
            if key == KeyCode(char="w"):
                twist.linear.x = 1.0
                twist.angular.z = 0.0
                twist.linear.y = 0.0
                print("hehe1")
            elif key == KeyCode(char="s"):
                twist.linear.x = -1.0
                twist.angular.z = 0.0
                twist.linear.y = 0.0
                print("hehe2")
            # elif key == KeyCode(char="d"):
            #     twist.linear.y = -1.0
            #     twist.angular.z = 0.0
            #     twist.linear.x = 0.0
            #     print("hehe3")
            # elif key == KeyCode(char="a"):
            #     twist.linear.y = 1.0
            #     twist.angular.z = 0.0
            #     twist.linear.x = 0.0
            #     print("hehe4")
            elif key == KeyCode(char="a"):
                twist.angular.z = 2.0
                twist.linear.x = twist.linear.y = 0.0
                print("hehe5")
            elif key == KeyCode(char="d"):
                twist.angular.z = -2.0
                twist.linear.x = twist.linear.y = 0.0
            elif key == KeyCode(char="z"):
                twist.angular.z = twist.linear.x = twist.linear.y = 0.0
            self.pub.publish(twist)
            
        except AttributeError:
            print('special key pressed: {0}'.format(
                key))

    def on_release(self,key):
        print('Key released: {0}'.format(
            key))
        twist.angular.z = twist.linear.x = twist.linear.y = 0.0
        self.pub.publish(twist)
        self.rate.sleep()
        if key == Key.esc:

            return False

    def main(self):
        with Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()

if __name__ == '__main__':
    try:
        obj=Main()
    except rospy.ROSInterruptException:
        pass
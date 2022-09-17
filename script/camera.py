#!/usr/bin/env python3

from operator import truediv
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import apriltag
from geometry_msgs.msg import Twist
import math


class image_converter:

  def __init__(self):
    rospy.init_node('image_converter', anonymous=True)
    self.pub = rospy.Publisher('grid_robot/cmd_vel',Twist, queue_size=10)
    self.image_sub = rospy.Subscriber('head/image_raw',Image,self.callback)
    self.bridge = CvBridge()
    print("X and Y cordinated of the destination: ")

    self.cordinates = [ int(x) for x in input().split()]
    while not rospy.is_shutdown():
    
      self.apriltag()
    
  def callback(self,data):
    try:
      self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

  def apriltag(self):

    self.gray = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2GRAY)
    #detecting april tag
    self.options = apriltag.DetectorOptions(families="tag36h11")
    self.detector = apriltag.Detector(self.options)
    self.results = self.detector.detect(self.gray)

    for r in self.results:
      
      # extract the bounding box (x, y)-coordinates for the AprilTag
      # and convert each of the (x, y)-coordinate pairs to integers
      (ptA, ptB, ptC, ptD) = r.corners
      ptB = (int(ptB[0]), int(ptB[1]))
      ptC = (int(ptC[0]), int(ptC[1]))
      ptD = (int(ptD[0]), int(ptD[1]))
      ptA = (int(ptA[0]), int(ptA[1]))

      # Centre of the front part
      self.ptM = (int(ptC[0]/2+ptB[0]/2),int(ptC[1]/2+ ptB[1]/2))

      # draw the bounding box of the AprilTag detection
      cv2.line(self.cv_image, ptA, ptB, (0, 255, 0), 2)
      cv2.line(self.cv_image, ptB, ptC, (0, 255, 0), 2)
      cv2.line(self.cv_image, ptC, ptD, (0, 255, 0), 2)
      cv2.line(self.cv_image, ptD, ptA, (0, 255, 0), 2)

      # draw the center (x, y)-coordinates of the AprilTag
      (self.cX, self.cY) = (int(r.center[0]), int(r.center[1]))
      self.centre = (self.cX,self.cY)
      cv2.circle(self.cv_image, self.centre, 2, (0, 0, 255), -1)

      #draw the center of the front part
      cv2.circle(self.cv_image, (self.ptM[0], self.ptM[1]), 2, (0, 0, 255), -1)

      # draw the tag family on the image
      cv2.putText(self.cv_image, 'A', (ptA[0], ptA[1]),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
      cv2.putText(self.cv_image, 'B', (ptB[0], ptB[1]),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
      cv2.putText(self.cv_image, 'C', (ptC[0], ptC[1]),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
      cv2.putText(self.cv_image, 'D', (ptD[0], ptD[1]),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

      self.movement()

  def movement(self):

    #input
    final = (self.cordinates[0], self.cordinates[1])

    #draw a line to the input point
    cv2.line(self.cv_image, self.centre, final, (0, 255, 0), 5)

   
    inv_m1 = math.atan2((self.ptM[1]-self.cY),(self.ptM[0]-self.cX))
    inv_m2 = math.atan2((self.cordinates[1]-self.cY), (self.cordinates[0]-self.cX))

    if abs(final[0]-self.centre[0])<1:
      if abs(final[1]-self.centre[1])<1:
        twist.angular.z = twist.linear.x = twist.linear.y = 0.0
        #print("stop")

    elif inv_m1-inv_m2<-0.1:#clockwise
      twist.angular.z = -0.5
      twist.linear.x = twist.linear.y = 0.0
      #print("Clockwise")
    
    elif inv_m1-inv_m2>0.1:#anticlockwise
      twist.angular.z = 0.5
      twist.linear.x = twist.linear.y = 0.0
      #print("Anticlockwise")

    else:#straight
      twist.linear.x = 0.1
      twist.angular.z = 0.0
      twist.linear.y = 0.0
      #print("Forward")
    
    self.pub.publish(twist)
   
    cv2.imshow("Image", self.cv_image)

    cv2.waitKey(10)


if __name__ == '__main__':
    
    try:
      twist = Twist()
      image_converter()
    except KeyboardInterrupt:
      print("Shutting down")
    cv2.destroyAllWindows()
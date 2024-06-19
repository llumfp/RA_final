#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import rospy
import cv2
import time

from std_msgs.msg import String
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge  import CvBridge, CvBridgeError
from red_squares import *

class RectDetector:

    def __init__(self,thr_min,thr_max,thr_min2, thr_max2, blur=15, detection_window=None):
        self.set_threshold(thr_min,thr_max, thr_min2, thr_max2)
        self.set_blur(blur)
        self.detection_window = detection_window
        self.bridge = CvBridge()
        self.rect_point = Point()
        self._t0 = time.time()
            
        rospy.loginfo(">> Publishing image to topic image")
        self.image_pub = rospy.Publisher("/red/image",Image,queue_size=1) #Publisher de la imatge crua
        self.mask_pub = rospy.Publisher("/red/image_mask",Image,queue_size=1)  #Publisher de la imatge amb la màscara
        
        rospy.loginfo(">> Publishing position to topic keypoint")
        self.keypoint_pub  = rospy.Publisher("/red/keypoint",Point,queue_size=1)  #Publisher del keypoint del rectangle com un Point
        
        rospy.loginfo("<< Subscribed to topic /camera/image")
        self.image_sub = rospy.Subscriber("/camera/image",Image, self.callback)  #Ens subscribim al node on la càmara del raspi publica cada frame amb la funció callback
        
    def set_threshold(self, thr_min, thr_max, thr_min2, thr_max2):
        self._threshold = [thr_min, thr_max, thr_min2, thr_max2]
        
    def set_blur(self, blur):
        self._blur = blur
  
    def callback(self,data):
        #--- Assuming image is 320x240
        #rospy.loginfo(data)
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
        
        #rospy.loginfo(cv_image)
        #--- Detect rectangles
        #cv2.imshow("image", cv_image)
        keypoint, mask   = detect_largest_red_object(cv_image,low_th=self._threshold[0],up_th=self._threshold[1], low_th2 = self._threshold[2], up_th2 = self._threshold[3], blur=self._blur, imshow=False, search_window=self.detection_window)
        
        rospy.loginfo(keypoint)
        #--- Draw search window and rectangles
        cv_image = blur_outside(cv_image, 3, self.detection_window)
        cv_image = draw_window(cv_image, self.detection_window, line=1)
        cv_image = draw_frame(cv_image)
        cv_image = draw_rectangles(cv_image, keypoint) 
        
        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
            self.mask_pub.publish(self.bridge.cv2_to_imgmsg(mask, "8UC1"))
        except CvBridgeError as e:
            print(e)            

        #--- We are simply getting the first result
        x = keypoint.pt[0]
        y = keypoint.pt[1]
        s = keypoint.size
        rospy.loginfo("s = %3d   x = %3d  y = %3d" % (s, x, y))

        #--- Find x and y position in camera adimensional frame
        x, y = get_rectangle_relative_position(cv_image, keypoint)

        self.rect_point.x = x
        self.rect_point.y = y
        
        self.keypoint_pub.publish(self.rect_point) 
        self._t0 = time.time()
           

    def run(self):
        rate = rospy.Rate(5)
        while not rospy.is_shutdown():
            rate.sleep() 


if __name__ == '__main__':
    
    red_min = np.array([0, 100, 100])
    red_max = np.array([10, 255, 255])
    red_min2 = np.array([170, 100, 100])
    red_max2 = np.array([180, 255, 255])
    blur    = 3
    x_min   = 0.25
    x_max   = 0.25
    y_min   = 0.75
    y_max   = 0.75
    detection_window = [x_min, y_min, x_max, y_max]   
    
    rospy.loginfo("Publish node inicialitzat")
    rospy.init_node('publish_node', anonymous=True)
    ic = RectDetector(red_min, red_max, red_min2, red_max2, blur, detection_window)
    ic.run()


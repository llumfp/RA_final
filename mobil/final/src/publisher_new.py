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
from red_new import *

class RectDetector:

    def __init__(self,thr_min,thr_max,thr_min2, thr_max2, blur=15, detection_window=None, real_object_width=None, focal_length=None,
                    cx = 0, cy = 0, fx = 0, fy = 0):
        
        self.set_threshold(thr_min,thr_max, thr_min2, thr_max2)
        self.set_blur(blur)
        self.detection_window = detection_window
        self.bridge = CvBridge()
        self.rect_point = Point()
        self.real_object_width = real_object_width
        self.focal_length = focal_length
        self.cx = cx
        self.cy = cy
        self.fx = fx
        self.fy = fy
            
        rospy.loginfo(">> Publishing image to topic image")
        self.image_pub = rospy.Publisher("/red/image",Image,queue_size=1) #Publisher de la imatge crua
        self.mask_pub = rospy.Publisher("/red/image_mask",Image,queue_size=1)  #Publisher de la imatge amb la màscara
        
        rospy.loginfo(">> Publishing position to topic location")
        self.keypoint_pub  = rospy.Publisher("/red/location",Point,queue_size=1)  #Publisher del keypoint del rectangle com un Point
        
        rospy.loginfo("<< Subscribed to topic /camera/image")
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image, self.callback)  #Ens subscribim al node on la càmara del raspi publica cada frame amb la funció callback
        
    def set_threshold(self, thr_min, thr_max, thr_min2, thr_max2):
        self._threshold = [thr_min, thr_max, thr_min2, thr_max2]
        
    def set_blur(self, blur):
        self._blur = blur
  
    def callback(self,data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
        
        location, mask  = detect_largest_red_object(cv_image,low_th=self._threshold[0], up_th=self._threshold[1], low_th2=self._threshold[2], up_th2=self._threshold[3], 
                                                    blur=self._blur, imshow=False, search_window=self.detection_window, real_object_width=self.real_object_width, 
                                                    focal_length=self.focal_length, cx=self.cx, cy =self.cy, fx=self.fx, fy=self.fy)
                
        self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
        self.mask_pub.publish(self.bridge.cv2_to_imgmsg(mask, "8UC1"))

        rospy.loginfo("x = %3d   y = %3d  z = %3d" % (location[0], location[1], location[2]))

        self.rect_point.x = location[0]
        self.rect_point.y = location[1]
        self.rect_point.z = location[2]
        
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
    real_object_width=100 #mm
    focal_length=3.6 #mm
    cx = 199.2686
    cy = 155.2533
    fx = 322.0704
    fy = 320.8673
    
    rospy.loginfo("Publish node inicialitzat")
    rospy.init_node('publish_node', anonymous=True)
    ic = RectDetector(red_min, red_max, red_min2, red_max2, blur, detection_window, real_object_width, focal_length, cx, cy, fx, fy)
    ic.run()


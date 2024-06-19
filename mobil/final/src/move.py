#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math, time
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
import time

K_LAT_DIST_TO_STEER = 0.3

def saturate(value, min, max):
    if value <= min: return(min)
    elif value >= max: return(max)
    else: return(value)

class MoveKobuki():
    def __init__(self):
         
        self.rect_x = 0.0
        self.rect_y = 0.0
        self._time_detected = 0.0
        
        self.keypoint_sub = rospy.Subscriber("/red/keypoint", Point, self.update_rect)
        rospy.loginfo("Subscribers set")
        
        self.pub_vel = rospy.Publisher("/cmd_vel", Twist, queue_size=5)
        rospy.loginfo("Publisher set")
        
        self._message = Twist()
        
        self._time_steer = 0
        self._steer_sign_prev = 0
        
        self.gira = False

    def is_detected(self):
        rospy.loginfo(time.time())
        rospy.loginfo(self._time_detected)
        
        if time.time() - self._time_detected > 4:
            self.gira = True
            return False
        else:
            return(time.time() - self._time_detected < 2.5)
        
    def update_rect(self, message):
        rospy.loginfo("Function update called")
        if message.x != 0 or message.y != 0:
            self.rect_x = message.x
            self.rect_y = message.y
            self._time_detected = time.time()
        #rospy.loginfo(time.time())
        #rospy.loginfo(self._time_detected)
    
    def get_control_action(self):
        steer_action    = 0.0
        throttle_action = 0.0
        
        rospy.loginfo("action_control")
        #rospy.loginfo(self._time_detected)
        #rospy.loginfo(self.is_detected())
        if self.is_detected():
            #--- Apply steering, proportional to how close is the object
            steer_action   =-K_LAT_DIST_TO_STEER*self.rect_x
            steer_action   = saturate(steer_action, -1.5, 1.5)
            rospy.loginfo("Steering command %.2f"%steer_action) 
            throttle_action = 0.2 
        elif self.gira:
            steer_action = 1
            throttle_action = 0
        return (steer_action, throttle_action)
        

def run():
    rospy.init_node('move_node', anonymous = True)
    chase_rect = MoveKobuki()
    
    rate_hz = 1  # Puedes ajustar el valor según necesites
    rate_duration = 1.0 / rate_hz

    ctrl_c = False
    def shutdownhook():
        # works better than the rospy.is_shut_down()
        rospy.loginfo("shutdown time!")
        nonlocal ctrl_c
        ctrl_c = True

    rospy.on_shutdown(shutdownhook) 
    while not ctrl_c:
        steer_action, throttle_action = chase_rect.get_control_action() 
            
        rospy.loginfo("Steering = %3.1f"%(steer_action))
        rospy.loginfo("Throttle action = %3.1f"%(throttle_action))      
        chase_rect._message.linear.x  = throttle_action
        chase_rect._message.angular.z = steer_action
            
        chase_rect.pub_vel.publish(chase_rect._message)
        
        time.sleep(rate_duration)

if __name__ == "__main__":
    try:    
        run()
    except rospy.ROSInterruptException:
        pass
    

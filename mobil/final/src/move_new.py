#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib import SimpleActionClient
import tf

def saturate(value, min, max):
    if value <= min:
        return min
    elif value >= max:
        return max
    else:
        return value

class MoveKobuki():
    def __init__(self):
        self.rect_x = 0.0
        self.rect_y = 0.0
        self.rect_z = 0.0
        self._time_detected = 0.0
        self.following_goal = False  # Estado que indica si se está siguiendo un objetivo
        
        self.location_sub = rospy.Subscriber("/red/location", Point, self.update_rect)
        rospy.loginfo("Subscribers set")

        #self.move_base_client = SimpleActionClient('/move_base', MoveBaseAction)
        #rospy.loginfo("Waiting for move_base action server...")
        #self.move_base_client.wait_for_server()
        
        self.publish_goal = rospy.Publisher("/red/goal", Point, queue_size = 1)

    def update_rect(self, message):
        rospy.loginfo("Function update called")
        self.rect_x = message.x
        self.rect_y = message.y
        self.rect_z = message.z
        self._time_detected = time.time()
        self.send_goal()
        
    def is_detected(self):
        rospy.loginfo(time.time())
        rospy.loginfo(self._time_detected)
        return (time.time() - self._time_detected < 1.0)
        
    def send_goal(self):
        rospy.loginfo("New goal?")
        if not self.following_goal:  # Comprueba si ya se está siguiendo un objetivo
            rospy.loginfo("New goal!")
            rospy.loginfo("Sending goal to Move Base")
            
            punt = Point()
            punt.x = self.rect_x
            punt.y = self.rect_y
            punt.z = self.rect_z
            self.publish_goal.publish(punt)
            rospy.loginfo("Punt publicat")
            self.following_goal = True

    def done_callback(self, status, result):
        rospy.loginfo("Goal reached or canceled")
        self.following_goal = False
    """
    def get_control_action(self):
        rospy.loginfo("Control action")
        if self.is_detected():
            self.send_goal_to_move_base(self.rect_x, self.rect_y, self.rect_z)
    """
def run():
    rospy.init_node('move_node', anonymous=True)
    chase_rect = MoveKobuki()
    
    rate_hz = 1
    rate_duration = 1.0 / rate_hz

    ctrl_c = False
    def shutdownhook():
        rospy.loginfo("shutdown time!")
        nonlocal ctrl_c
        ctrl_c = True

    rospy.on_shutdown(shutdownhook)
    while not ctrl_c:
        time.sleep(rate_duration)

if __name__ == "__main__":
    try:
        run()
    except rospy.ROSInterruptException:
        pass

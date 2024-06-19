#! /usr/bin/env python3

import rospy
import time
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseResult, MoveBaseFeedback

from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point


# definition of the feedback callback. This will be called when feedback
# is received from the action server
# it just prints a message indicating a new message has been received


def feedback_callback(feedback):
    print('[Feedback] Going to Goal Pose...')


class Mover():
    def __init__(self):
	
        self.goal = rospy.Subscriber("/red/goal", Point, self.go_goal)
        rospy.loginfo("Subscribers set")
        
        #self.publish_goal = rospy.Publisher("/red/goal", Point, self.send_goal)

    def go_goal(self, message):

        rospy.loginfo("Setting the goal")
        client = actionlib.SimpleActionClient('/move_base', MoveBaseAction)
        # waits until the action server is up and running
        client.wait_for_server()
        # creates a goal to send to the action server
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'base_link'
        goal.target_pose.pose.position.x = message.x
        goal.target_pose.pose.position.y = message.y
        goal.target_pose.pose.position.z = 0.0
        goal.target_pose.pose.orientation.x = 0.0
        goal.target_pose.pose.orientation.y = 0.0
        goal.target_pose.pose.orientation.z = 0.75
        goal.target_pose.pose.orientation.w = 0.66
        client.send_goal(goal, feedback_cb=feedback_callback)
        client.wait_for_result()
        print('[Result] State: %d'%(client.get_state()))

def run():
    rospy.init_node('move_base_action_client')
    chase_rect = Mover()

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


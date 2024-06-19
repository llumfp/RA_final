#! /usr/bin/env python3

import rospy
import time
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseResult, MoveBaseFeedback

from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point, PointStamped
import tf

# definition of the feedback callback. This will be called when feedback
# is received from the action server
# it just prints a message indicating a new message has been received


def feedback_callback(feedback):
    print('[Feedback] Going to Goal Pose...')


class Mover():
    def __init__(self):
        self.goal = rospy.Subscriber("/red/goal", Point, self.go_goal)
        rospy.loginfo("Subscribers set")
        self.tf_listener = tf.TransformListener()

    def go_goal(self, message):
        rospy.loginfo("Setting the goal")
        client = actionlib.SimpleActionClient('/move_base', MoveBaseAction)
        client.wait_for_server()

        success = False
        for _ in range(10):
            try:
                self.tf_listener.waitForTransform("/base_link", "/map", rospy.Time(), rospy.Duration(1.0))
                (trans, rot) = self.tf_listener.lookupTransform("/map", "/base_link", rospy.Time(0))
                success = True
                break
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                rospy.logwarn("TF Exception, retrying...")
                rospy.sleep(1.0)

        if not success:
            rospy.logerr("Unable to obtain transformation between /base_link and /map")
            return

        rospy.loginfo("Transformation obtained")

        # Transformar las coordenadas del objetivo desde el marco del robot al marco del mapa
        goal_point = PointStamped()
        goal_point.header.frame_id = "/base_link"
        goal_point.header.stamp = rospy.Time(0)
        goal_point.point.x = message.x
        goal_point.point.y = message.y
        goal_point.point.z = 0.0

        try:
            map_point = self.tf_listener.transformPoint("/map", goal_point)
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            rospy.logerr("TF Exception")
            return
        
        rospy.loginfo(f"Map coordinates: x={map_point.point.x}, y={map_point.point.y}")
        
        rospy.loginfo("Transformation applied")

        # Crear y enviar el objetivo al cliente de acción
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.pose.position.x = map_point.point.x
        goal.target_pose.pose.position.y = map_point.point.y
        goal.target_pose.pose.position.z = 0.0
        goal.target_pose.pose.orientation.x = 0.0
        goal.target_pose.pose.orientation.y = 0.0
        goal.target_pose.pose.orientation.z = 0.75
        goal.target_pose.pose.orientation.w = 0.66
        
        rospy.loginfo("Goal sent")
        
        client.send_goal(goal, feedback_cb=feedback_callback)
        client.wait_for_result()
        
        print('[Result] State: %d' % client.get_state())

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


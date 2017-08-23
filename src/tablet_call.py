#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Empty
import time

def talker():
    pub = rospy.Publisher('roah_rsbb/tablet/call', Empty, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    time.sleep(1)
    pub.publish()
    time.sleep(2)


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

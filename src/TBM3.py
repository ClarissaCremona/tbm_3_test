#! /usr/bin/env python

# Title : TBM3_demo.py
# Author : Clarissa Cremona
# Date : 21/08/2017
# Version : 1.0

##############################################################################################################
#   In order for this demo to work the RSBB and iot_bridge must be running.
# 
#   This Python script demos TBM3 from ERL-Service tournament. It can be run by using the terminal command:
#       $ rosrun tbm_3_test TBM3_demo.py
#   
#   In this program, Pepper asks a user if he/she needs any assistance. The user responds with "Switch on the 
#   kitchen light". Press Enter and Pepper will then switch on the kitchen light.
##############################################################################################################

import qi
import argparse
import sys
import rospy
import time
from std_msgs.msg import Empty

global session

def task3(session):

    # Getting the service ALRobotPosture
    ALRobotPosture = session.service("ALRobotPosture") 

    # Go to initial position
    ALRobotPosture.goToPosture("StandInit", 0.5) # return to initial position

    # Getting the service ALAnimatedSpeech
    ALAnimatedSpeech = session.service("ALAnimatedSpeech")

    # Pepper proposal
    ALAnimatedSpeech.say("Hello. How may I be of assistance?")

    # Getting the service ALDialog
    ALDialog = session.service("ALDialog")
    ALDialog.setLanguage("English")
   
    # writing topics' qichat code as text strings 
    topic_content_1 = ('topic: ~devices()\n'
                       'language: enu\n'
                       'concept:(device) ["bedroom light" "kitchen light"]\n'
                       'u: (Switch on the _~device) Ok! So I will switch on the $1 correct?\n'
                        'u1: (yes) Ok, I am doing that now.'
                        )

    # Loading the topics directly as text strings
    topic_name_1 = ALDialog.loadTopicContent(topic_content_1)

    # Activating the loaded topics
    ALDialog.activateTopic(topic_name_1)

    # Starting the dialog engine 
    ALDialog.subscribe('my_dialog_example')

    try:
        raw_input("\nPress Enter when finished to switch on the kitchen light:")
    finally:

        # stopping the dialog engine
        ALDialog.unsubscribe('my_dialog_example')

        # Deactivating topic
        ALDialog.deactivateTopic(topic_name_1)

        # now that the dialog engine is stopped and there are no more activated topics,
        # we can unload topic and free the associated memory
        ALDialog.unloadTopic(topic_name_1)

        # import necessary service files
        import std_srvs
        from std_srvs.srv import Empty

        # call service to switch on kitchen light
        rospy.wait_for_service('/devices/switch_1/on')
        try:
            time.sleep(3)
            switch_1 = rospy.ServiceProxy('/devices/switch_1/on', Empty)
            response = switch_1()
            #time.sleep(3)

        except rospy.ServiceException, e:
            print "Service call failed: %s"%e

def callback(data):
	task3(session)

def tablet_listener():
	print("Pepper is now waiting to be called from the tablet...")
	rospy.init_node('pepper_listener', anonymous=True) # create node to subscribe to topic
	rospy.Subscriber("roah_rsbb/tablet/call", Empty, callback) # subscribe to topic /iot_updates
	rospy.spin() # keeps python from exiting until node is stopped
    #print(data.value)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.121",
                        help="Robot's IP address. If on a robot or a local Naoqi - use '127.0.0.1' (this is the default value).")
    parser.add_argument("--port", type=int, default=9559,
                        help="port number, the default value is OK in most cases")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://{}:{}".format(args.ip, args.port))
    except RuntimeError:
        print ("\nCan't connect to Naoqi at IP {} (port {}).\nPlease check your script's arguments."
               " Run with -h option for help.\n".format(args.ip, args.port))
        sys.exit(1)

    while True:
    	tablet_listener()

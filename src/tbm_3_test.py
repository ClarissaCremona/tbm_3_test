#!/usr/bin/env python
# Title : pepper_iot.py
# Author : Clarissa Cremona
# Date : 09/06/2017
# Version : 1.0

import rospy, qi, argparse
import os
import sys
import time
import naoqi
from naoqi import *
from diagnostic_msgs.msg import KeyValue # this is the message type /iot_updates uses

#class myModule(ALModule):
def dialog1():
    ALDialog = ALProxy("ALDialog", "pepper.local", 9559)
    topic_content = ('topic: ~task3()\n'
					'language: enu\n'
					'concept:(device) ["kitchen light"]\n'
                    'u: (Switch on the _~device) Ok! So I will switch on the $1 correct?^stopTag(body language)\n'
                        'u1: (yes) Ok, I am doing that now.\n'
                        'u1: (no) Ok then. I will not do that\n'
                    'u: (Switch off the _~device) Ok! So I will switch off the $1 correct?^stopTag(body language)\n'
                        'u1: (yes) Ok, I am doing that now.\n'
                        'u1: (no) Ok then. I will not do that.'
                        )
                        
    topic_name = ALDialog.loadTopicContent(topic_content)
    ALDialog.activateTopic(topic_name)
    ALDialog.subscribe('task3_dialog')
    time.sleep(20)
    ALDialog.unsubscribe('task3_dialog')
    ALDialog.deactivateTopic(topic_name)
    ALDialog.unloadTopic(topic_name)
    basicProxy.setEnabled(False)
    postureProxy.goToPosture("StandInit", 0.5)
    return

def speak():
    animatedProxy.say("LA LA LA")

# def callback(data):
#     import std_srvs
# 	from std_srvs.srv import Empty
#     #	print("in callback")
#     #	animatedProxy.say("Someone is at the door")
# 	rospy.wait_for_service('/devices/switch_1/on')
# 	try:
# 		switch_1 = rospy.ServiceProxy('/devices/switch_1/on', Empty)
# 		response = switch_1()

# 	except rospy.ServiceException, e:
# print "Service call failed: %s"%e

def help():
    basicProxy.setTrackingMode("MoveContextually") # track human with head
    animatedProxy.say("Hello. How may I be of assistance?")
    dialog1()
    # postureProxy.goToPosture("StandInit", 0.5) # return to initial position
    # motionProxy.moveTo(1.0, 0.0, 0.0) # move forewards
    # postureProxy.goToPosture("StandInit", 0.5) # return to initial position

if __name__ == '__main__':
    from naoqi import ALProxy
    # Create a local broker, connected to the remote naoqi
    broker = ALBroker("pythonBroker", "192.168.1.63", 9999, "pepper.local", 9559)
    #global newModule
    #newModule = myModule("newModule")
    tts = ALProxy("ALTextToSpeech", "pepper.local", 9559) # initialise speech proxy
    tts.setParameter("speed", 100) # set speed of speech
    animatedProxy = ALProxy("ALAnimatedSpeech", "pepper.local", 9559) # initialise animated speech proxy
    postureProxy = ALProxy("ALRobotPosture", "pepper.local", 9559) # initialise posture proxy
    motionProxy = ALProxy("ALMotion", "pepper.local", 9559) # initialise motion proxy
    tabletProxy = ALProxy("ALTabletService", "pepper.local", 9559)
    #recogProxy = ALProxy("ALSpeechRecognition", "pepper.local", 9559) # initialise speech recognition proxy

    basicProxy = ALProxy("ALBasicAwareness", "pepper.local", 9559) # initialise basic awareness proxy
    basicProxy.setEnabled(True) # enable basic awareness # set tracking mode to move
    basicProxy.setEngagementMode("FullyEngaged")

    #recogProxy.subscribe("Test_ASR")
    #memProxy = ALProxy("ALMemory","pepper.local",9559)
    #memoryProxy.subscribeToEvent(event_name, "newModule", "Dialog/Answered")
    help()
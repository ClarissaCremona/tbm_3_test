#! /usr/bin/env python

# Title : TBM3_demo.py
# Author : Clarissa Cremona
# Date : 23/08/2017
# Version : 1.0


"""
Script to switch kitchen light on with voice activation
"""

from naoqi import *
import time
check = 0
import qi
import argparse
import sys
import rospy
import time
from std_msgs.msg import Empty
variableName=0
variableName1=0

# create python module
class myModule(ALModule):
  """python class myModule test auto documentation: comment needed to create a new python module"""


  def on(self, strVarName, value):
    """callback when data change"""
    import std_srvs
    from std_srvs.srv import Empty

    print "strVarName", strVarName
    print "value " , value

    try:
        #time.sleep(3)
        switch_1 = rospy.ServiceProxy('/devices/switch_1/on', Empty)
        switch_2 = rospy.ServiceProxy('/devices/switch_2/on', Empty)
        if value == "1":
            print "Switching kitchen light on"
            response = switch_1()
        elif value == "2":
            print "Switching bedroom light on"
            response = switch_2()
        #time.sleep(3)

    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

  def off(self, strVarName, value):
    """callback when data change"""
    import std_srvs
    from std_srvs.srv import Empty

    print "strVarName", strVarName  
    print "value " , value
    try:
        #time.sleep(3)
        switch_1 = rospy.ServiceProxy('/devices/switch_1/off', Empty)
        switch_2 = rospy.ServiceProxy('/devices/switch_2/off', Empty)
        if value == "4":
            print "Switching kitchen light off"
            response = switch_1()
        elif value == "3":
            print "Switching bedroom light off"
            response = switch_2()
        #time.sleep(3)

    except rospy.ServiceException, e:
        print "Service call failed: %s"%e
      

  def _pythonPrivateMethod(self, param1, param2, param3):
    global check

  def dialog(self):
        global device_on
        
        ALDialog.setLanguage("English")
        ALAnimatedSpeech.say("How may I be of assistance?")
        # writing topics' qichat code as text strings 
        topic_content_1 = ('topic: ~devices1()\n'
                        'language: enu\n'
                        'concept:(device) ["bedroom light" "kitchen light"]\n'
                        'u: (Switch on the _~device) Ok! So I will switch on the $1 correct? $device=$1\n'
                            'u1: (yes) $device=="bedroom light" Ok, I am doing that now. $device_on=2\n'
                            'u1: (yes) $device=="kitchen light" Ok, I am doing that now. $device_on=1\n'
                            'u1: (no) Ok then. I will not do that\n'
                        'u: (Switch off the _~device) Ok! So I will switch off the $1 correct?$device=$1\n'
                            'u1: (yes) $device=="bedroom light" Ok, I am doing that now. $device_off=3\n'
                            'u1: (yes) $device=="kitchen light" Ok, I am doing that now. $device_off=4\n'
                            'u1: (no) Ok then. I will not do that.\n'
                        'u: (Goodbye) Goodbye!'
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
            exit(1)
        


broker = ALBroker("pythonBroker","192.168.1.63",9999,"192.168.1.121",9559)


# call method
try:

  pythonModule = myModule("pythonModule")
  ALMemory = ALProxy("ALMemory")
  ALAnimatedSpeech = ALProxy("ALAnimatedSpeech")
  ALRobotPosture = ALProxy("ALRobotPosture")
  ALDialog = ALProxy("ALDialog")
  #prox.insertData("val",1) # forbidden, data is optimized and doesn't manage callback
  ALMemory.subscribeToEvent("device_on","pythonModule", "on") #  event is case sensitive !
  ALMemory.subscribeToEvent("device_off", "pythonModule", "off")
  ALRobotPosture.goToPosture("StandInit", 0.5)
  # call service to switch on kitchen light
  rospy.wait_for_service('/devices/switch_1/on')
  # call service to switch off kitchen light
  rospy.wait_for_service('/devices/switch_2/on')
  pythonModule.dialog()

except Exception,e:
  print "error"
  print e
  exit(1)

while (1):
  time.sleep(2)
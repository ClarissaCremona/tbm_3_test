#! /usr/bin/env python

import qi
import argparse
import sys
import rospy

def task3(session):
    """
    Pepper asks the user if it can be of any assistance
    """
    ALAnimatedSpeech = session.service("ALAnimatedSpeech")
    
    ALAnimatedSpeech.say("Hello can i help you?")
    # Getting the service ALDialog
    ALDialog = session.service("ALDialog")
    ALDialog.setLanguage("English")
    stop = 1
    # writing topics' qichat code as text strings (end-of-line characters are important!)
    topic_content_1 = ('topic: ~dumdum1()\n'
                       'language: enu\n'
                       'concept:(device) ["bedroom light" "kitchen light"]\n'
                       'u: (Switch on the _~device) Ok! So I will switch on the $1. ^switchFocus(test1/behavior_1)\n'
                        )
    # topic_content_2 = ('topic: ~dummy_topic()\n'
    #                    'language: enu\n'
    #                    'concept:(device) ["bedroom light" "kitchen light"]\n'
    #                    'u: (Switch off the _~device) Ok! So I will switch off the $1 correct?\n'
    #                     'u1: (yes) Ok, I am doing that now.'
    #                     )


    # Loading the topics directly as text strings
    topic_name_1 = ALDialog.loadTopicContent(topic_content_1)
    #topic_name_2 = ALDialog.loadTopicContent(topic_content_2)

    # Activating the loaded topics
    ALDialog.activateTopic(topic_name_1)
    #ALDialog.activateTopic(topic_name_2)

    # Starting the dialog engine - we need to type an arbitrary string as the identifier
    # We subscribe only ONCE, regardless of the number of topics we have activated
    ALDialog.subscribe('my_dialog_example')

    try:
        raw_input("\nSpeak to the robot using rules from both the activated topics. Press Enter when finished:")
    finally:
        # add code to actually switch on light
        print(stop)
        # stopping the dialog engine
        ALDialog.unsubscribe('my_dialog_example')

        # Deactivating all topics
        ALDialog.deactivateTopic(topic_name_1)
        #ALDialog.deactivateTopic(topic_name_2)

        # now that the dialog engine is stopped and there are no more activated topics,
        # we can unload all topics and free the associated memory
        ALDialog.unloadTopic(topic_name_1)
        #ALDialog.unloadTopic(topic_name_2)


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
    ALMemory = session.service("ALMemory")
    task3(session)
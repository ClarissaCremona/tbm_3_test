#! /usr/bin/env python

#######################################################################################
# This program will test the speech recognition                                       #
#                                                                                     #
#######################################################################################


import qi
import argparse
import sys
import time


def main(session):
    """
    This example uses the ALSpeechRecognition module.
    """
    # Get the service ALSpeechRecognition.

    asr_service = session.service("ALSpeechRecognition")

    asr_service.setLanguage("English")

    # Example: Adds "yes", "no" and "please" to the vocabulary (without wordspotting)
    vocabulary = ["yes", "no", "switch on the bedroom light"]
    asr_service.setVocabulary(vocabulary, False)

    # Start the speech recognition engine with user Test_ASR
    asr_service.subscribe("Test_ASR")
    print 'Speech recognition engine started'
    time.sleep(20)
    asr_service.unsubscribe("Test_ASR")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="pepper.local",
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
    main(session)
#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64

import tty
import termios
import sys
import signal
import math

def get_char():
    # Function to get a single character from the user input
    file_descriptor = sys.stdin.fileno()
    old_settings = termios.tcgetattr(file_descriptor)

    try:
        tty.setraw(sys.stdin.fileno())
        char = sys.stdin.read(1)
    finally:
        termios.tcsetattr(file_descriptor, termios.TCSADRAIN, old_settings)

    return char

def handle_signal(signum, frame):
    # Signal handler to gracefully exit the program
    rospy.signal_shutdown('Program terminated')

def change_values():
    # Initialize the ROS node
    rospy.init_node('value_changer', anonymous=True)

    # Create a publisher for the topic
    pub_wl = rospy.Publisher('/my_robot/left_wheel_controller/command', Float64, queue_size=10)
    pub_wr = rospy.Publisher('/my_robot/right_wheel_controller/command', Float64, queue_size=10)

    # Create a ROS rate to control the publishing frequency
    rate = rospy.Rate(50)  # 50 Hz

    # Values
    wl = 0.0
    wr = 0.0

    # Register the signal handler for Ctrl + C
    signal.signal(signal.SIGINT, handle_signal)

    # Running
    running = True

    # Continuously publish the new value to the topic
    while not rospy.is_shutdown() and running:
        # Get the user input character
        char = get_char()

        if char == 'q':
            wl += 0.1
        elif char == 'a':
            wl -= 0.1
        elif char == 'w':
            wl += 0.1
            wr -= 0.1
        elif char == 's':
            wl -= 0.1
            wr += 0.1
        elif char == 'e':
            wr -= 0.1
        elif char == 'd':
            wr += 0.1
        elif char == 'r':
            wl *= 0.8
            wr *= 0.8
            if abs(wl) <= 0.5:
                wl = 0.0
            if abs(wr) <= 0.5:
                wr = 0.0
        elif char == 'f':
            running = False
        else:
            pass

        # Publish the message
        pub_wl.publish(wl)
        pub_wr.publish(wr)

        # print
        print(wl, wr)

        # Sleep to maintain the desired publishing frequency
        rate.sleep()

if __name__ == '__main__':
    try:
        change_values()
    except rospy.ROSInterruptException:
        pass

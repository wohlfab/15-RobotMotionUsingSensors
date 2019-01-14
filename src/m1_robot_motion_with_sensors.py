"""
This module demonstrates lets you practice implementing classes and the
wait-until-event pattern, in the context of robot motion that uses sensors.

Authors: David Mutchler, Vibha Alangar, Matt Boutell, Dave Fisher,
         Mark Hays, Amanda Stouder, Aaron Wilkin, their colleagues,
         and Brandon Wohlfarth.
"""  # DONE: 1. PUT YOUR NAME IN THE ABOVE LINE.

import ev3dev.ev3 as ev3
import time
import math


def main():
    """ Calls the other functions to test/demo them. """
    run_test_wait_for_seconds()
    run_test_init()
    run_test_go_and_stop()
    run_test_go_straight_for_seconds()
    run_test_go_straight_for_inches()
    run_test_go_straight_until_black()


def run_test_wait_for_seconds():
    """ Tests the   wait_for_seconds   function by calling it. """
    print()
    print('--------------------------------------------------')
    print('Testing the   wait_for_seconds   function:')
    print('--------------------------------------------------')

    wait_for_seconds()

    print('Here is a second test:')
    wait_for_seconds()


def wait_for_seconds(t):
    """ Prints Hello, waits for 3 seconds, then prints Goodbye. """
    # -------------------------------------------------------------------------
    # DONE: 2. With your instructor, implement and test this function.
    #   IMPORTANT:  Do NOT use the    time.sleep   function
    #               anywhere in this project.
    #               (Exception: Use it in test-functions to separate tests.)
    #
    #               Instead, use the   time.time   function
    #               that returns the number of seconds since "the Epoch"
    #               (January 1, 1970, 00:00:00 (UTC) on some platforms).
    #
    #   The testing code is already written for you (above, in main).
    #   NOTE: this function has nothing to do with robots,
    #   but its concepts will be useful in the forthcoming robot exercises.
    # -------------------------------------------------------------------------
    print('Hello')
    start = time.time()
    while True:
        current = time.time()
        if current - start >= 3:
            break
    print('Goodbye')

def run_test_init():
    """ Tests the   __init__   method of the SimpleRoseBot class. """
    print()
    print('--------------------------------------------------')
    print('Testing the   __init__   method of the SimpleRoseBot class:')
    print('--------------------------------------------------')
    # -------------------------------------------------------------------------
    # DONE: 3. Implement this function, then implement the   __init__   method
    #   of the SimpleRoseBot class, then use this function to test __init__.
    # -------------------------------------------------------------------------
    robot = SimpleRoseBot()

def run_test_go_and_stop():
    """ Tests the   go   and   stop   methods of the SimpleRoseBot class. """
    print()
    print('--------------------------------------------------')
    print('Testing the  go  and  stop  methods of the SimpleRoseBot class:')
    print('--------------------------------------------------')
    # -------------------------------------------------------------------------
    # DONE: 4. Implement this function, then implement the   go  and   stop
    #   methods of the SimpleRoseBot class, then use this function
    #   to test both   go   and   stop   at the same time.
    # -------------------------------------------------------------------------
    robot = SimpleRoseBot()
    robot.go(50, 50)
    start = time.time()
    while True:
        current = time.time()
        if current - start >= 2:
            break
    robot.stop()

def run_test_go_straight_for_seconds():
    """ Tests the   go_straight_for_seconds   method of SimpleRoseBot. """
    print()
    print('--------------------------------------------------')
    print('Testing the   go_straight_for_seconds   method of SimpleRoseBot:')
    print('--------------------------------------------------')
    # -------------------------------------------------------------------------
    # DONE: 5. Implement this function, then implement the
    #   go_straight_for_seconds   method of the SimpleRoseBot class,
    #   then use this function to test that method.
    # -------------------------------------------------------------------------
    robot = SimpleRoseBot()
    robot.go_straight_for_seconds(10, 50)

def run_test_go_straight_for_inches():
    """ Tests the   go_straight_for_inches   method of SimpleRoseBot. """
    print()
    print('--------------------------------------------------')
    print('Testing the   go_straight_for_inches   method of SimpleRoseBot:')
    print('--------------------------------------------------')
    # -------------------------------------------------------------------------
    # DONE: 6. Implement this function, then implement the
    #   go_straight_for_inches   method of the SimpleRoseBot class,
    #   then use this function to test that method.
    # -------------------------------------------------------------------------
    robot = SimpleRoseBot()
    robot.go_straight_for_distance(12, 50)

def run_test_go_straight_until_black():
    """ Tests the   go_straight_until_black   method of SimpleRoseBot. """
    print()
    print('--------------------------------------------------')
    print('Testing the   go_straight_until_black   method of SimpleRoseBot:')
    print('--------------------------------------------------')
    # -------------------------------------------------------------------------
    # TODO: 7. Implement this function, then implement the
    #   go_straight_until_black   method of the SimpleRoseBot class,
    #   then use this function to test that method.
    # -------------------------------------------------------------------------
    robot = SimpleRoseBot()
    robot.go_straight_until_black(50)

###############################################################################
# Put your   SimpleRoseBot    class here (below this comment).
# Your instructor may help you get started.
###############################################################################
class SimpleRoseBot(object):

    def __init__(self):
        self.left = Motor('B')
        self.right = Motor('C')
        self.color = ColorSensor(3)

    def go(self, left_speed, right_speed):
        self.left.turn_on(left_speed)
        self.right.turn_on(right_speed)

    def stop(self):
        self.left.turn_off()
        self.right.turn_off()

    def go_straight_for_secodnds(self, seconds, speed):
        self.go(speed, speed)
        start = time.time()
        while True:
            current = time.time()
            if current - start >= seconds:
                break
        self.stop()

    def go_straight_for_distance(self, inches, speed):
        self.go(speed, speed)
        self.left.reset_position()
        start = self.left.get_position()
        val = 0
        while True:
            current = self.left.get_position()
            if current <= start:
                val = (360 - start + current)*(1.3 * math.pi)/360 + val
                start = current
            else:
                val = (current - start)*(1.3 * math.pi)/360 + val
                start = current
            if val >= inches:
                break
        self.stop()

    def go_straight_until_black(self, speed):
        self.go(speed, speed)
        while True:
            color = self.color.get_reflected_light_intensity()
            if color >= 10:
                break
        self.stop()

###############################################################################
# The  Motor   and   ColorSensor classes.  USE them, but do NOT modify them.
###############################################################################
class Motor(object):
    WheelCircumference = 1.3 * math.pi

    def __init__(self, port):  # port must be 'B' or 'C' for left/right wheels
        self._motor = ev3.LargeMotor('out' + port)

    def turn_on(self, speed):  # speed must be -100 to 100
        self._motor.run_direct(duty_cycle_sp=speed)

    def turn_off(self):
        self._motor.stop(stop_action="brake")

    def get_position(self):  # Units are degrees (that the motor has rotated).
        return self._motor.position

    def reset_position(self):
        self._motor.position = 0


class ColorSensor(object):
    def __init__(self, port):  # port must be 3
        self._color_sensor = ev3.ColorSensor('in' + str(port))

    def get_reflected_light_intensity(self):
        # Returned value is from 0 to 100,
        # but in practice more like 3 to 90+ in our classroom lighting.
        return self._color_sensor.reflected_light_intensity


# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()

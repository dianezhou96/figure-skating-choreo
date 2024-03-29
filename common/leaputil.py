#####################################################################
#
# leaputil.py
#
# Copyright (c) 2017, Eran Egozy
#
# Released under the MIT License (http://opensource.org/licenses/MIT)
#
#####################################################################

# For complete documentation see:
# https://developer.leapmotion.com/documentation/v2/python/index.html

import platform
import sys
import numpy as np
import os

def fixLeapLib():
    import subprocess
    def runProcess(cmd):
        print cmd
        exe = cmd.split(' ') 
        p = subprocess.Popen(exe, stdout=subprocess.PIPE) #, stderr=subprocess.STDOUT)
        output = []
        while(True):
          retcode = p.poll() #returns None while subprocess is running
          line = p.stdout.readline()
          if(retcode is not None):
            break
          line = line.strip()
          if line:
            output.append(line)
        return output

    # the leap library to be fixed up:
    leap_lib = '../common/leap/osx/LeapPython.so'

    # find current location of python lib
    out = runProcess('otool -L %s' % leap_lib)
    cur_lib_loc = out[1].split(' ')[0]

    # create proper location of libpython2.7.dylib (assumes miniconda or brew installation)
    proper_lib_loc = sys.path[2].split('/lib/')[0] + '/lib/libpython2.7.dylib'
    if not os.path.exists(proper_lib_loc) :
        print 'Error:', proper_lib_loc, 'does not exist when trying to patch LeapPython.so'

    if cur_lib_loc != proper_lib_loc:
        print 'modifying:'
        out = runProcess('install_name_tool -change %s %s %s' % (cur_lib_loc, proper_lib_loc, leap_lib))
        print out
    else:
        print 'LeapPython.so is already OK'

# Find the right library to load based on platform
if platform.system() == 'Windows':
    sys.path.append('../common/leap/x64')
elif platform.system() == 'Darwin':
    sys.path.append('../common/leap/osx')
    fixLeapLib()

import Leap


# Return 3 lines of text about status of leap motion controller
def leap_info(leap):
    text = ''
    text += "Leap Service Connected:%d\n" % leap.is_service_connected()
    text += "Leap Connected:%d\n" % leap.is_connected
    text += "Leap Has Focus:%d\n" % leap.has_focus
    return text


# Convert leap position into a numpy array
def pt_to_array(pos):
    return np.array((pos[0], pos[1], pos[2]))


# Return the palm position of one hand (front-most hand).
# Returns (0,0,0) if no hand is found
def leap_one_palm(frame):
    if frame.hands.is_empty:
        return np.zeros(3)
    hand = frame.hands.frontmost
    pos = hand.palm_position
    return pt_to_array(pos)


# Return the plam positions of two hands as a tuple (left, right)
# Returns (0,0,0) for a hand-not-found
def leap_two_palms(frame):
    left = np.zeros(3)
    right = np.zeros(3)
    if len(frame.hands) == 1:
        if frame.hands[0].is_left:
            left = frame.hands[0].palm_position
        else:
            right = frame.hands[0].palm_position
    elif len(frame.hands) == 2:
        if frame.hands[0].is_left:
            left = frame.hands[0].palm_position
            right = frame.hands[1].palm_position
        else:
            left = frame.hands[1].palm_position
            right = frame.hands[0].palm_position
    return (pt_to_array(left), pt_to_array(right))


# Returns a tuple of 5 positions for the fingers of the frontmost hand
def leap_fingers_fingers(frame):
    if frame.hands.is_empty:
        return [np.zeros(3) for x in range(5)]
    hand = frame.hands.frontmost
    fingers = hand.fingers
    return [pt_to_array(f.tip_position) for f in fingers]


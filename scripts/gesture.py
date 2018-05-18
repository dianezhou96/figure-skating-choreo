import sys
sys.path.append('..')

from common.core import *
from common.gfxutil import topleft_label, topright_label
import common.leaputil
import Leap

import numpy as np

from moviepy.editor import AudioFileClip

from pprint import pprint

RANGE_MIN = np.array((-250.0, 50, -200))
RANGE_MAX = np.array((250.0, 600, 250))
def scale_point(pt):
	pt = pt_to_array(pt)
	pt = (pt - RANGE_MIN) / (RANGE_MAX - RANGE_MIN)
	pt = np.clip(pt, 0, 1)
	return pt

def pt_to_array(pos):
    return np.array((pos[0], pos[1], pos[2]))

class LeftHand:
	def __init__(self):
		self.num_fingers = -1

	def update(self, leap_frame):
		if len(leap_frame.hands) == 1 and leap_frame.hands[0].is_left:
			self.num_fingers = len(leap_frame.hands[0].fingers.extended())
		elif len(leap_frame.hands) == 2:
			if leap_frame.hands[0].is_left:
				self.num_fingers = len(leap_frame.hands[0].fingers.extended())
			else:
				self.num_fingers = len(leap_frame.hands[1].fingers.extended())
		else:
			self.num_fingers = -1
		return self.num_fingers


class RightHand:
	def __init__(self):
		self.zpos = 5

		self.can_cross = False
		self.can_circle = False

		self.threshold = 0.5

		self.state = 'None'

	def update(self, leap_frame):


		# Update location of hand
		if len(leap_frame.hands) == 1 and leap_frame.hands[0].is_right:
			self.zpos = scale_point(leap_frame.hands[0].palm_position)[1]
		elif len(leap_frame.hands) == 2:
			if leap_frame.hands[0].is_right:
				self.zpos = scale_point(leap_frame.hands[0].palm_position)[1]
			else:
				self.zpos = scale_point(leap_frame.hands[1].palm_position)[1]
		else:
			self.zpos = -1

		for gesture in leap_frame.gestures():
			if gesture.type is Leap.Gesture.TYPE_CIRCLE:
				circle = Leap.CircleGesture(gesture)
				complete_circles = circle.progress
				self.can_cross = False
				self.state = 'Circle #' + str(int(complete_circles))
				if complete_circles < 5:
					self.can_circle = True
				elif self.can_circle:
					print('spin')
					self.can_circle = False
					return 'spin'
				return None


		# Update jump
		crossed = False
		if self.zpos == -1:
			self.can_cross = False
		elif self.zpos > self.threshold:
			crossed = self.can_cross
			self.can_cross = False
		else:
			self.can_cross = True

		if crossed:
			print('jump')
			return 'jump'
		else:
			self.state = 'None' if self.zpos == -1 else 'Present'
			return None



class Gesture:
	def __init__(self):
		self.leap = Leap.Controller()
		self.leap.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
		self.left_hand = LeftHand()
		self.right_hand = RightHand()

		self.jumps = ['axel', 'salchow', 'toeloop', 'loop', 'flip', 'lutz']
		self.spins = ['combospin', 'layback']



	def recognize(self):
		leap_frame = self.leap.frame()
		left_fingers = self.left_hand.update(leap_frame)
		right_motion = self.right_hand.update(leap_frame)

		return left_fingers, right_motion

	def update(self, speech, speech_used):

		# left hand takes precedence over speech

		index, motion = self.recognize()

		if motion == 'jump':
			print(index)
			if index == -1 and not speech_used:
				index = self.jump_speech(speech)
			if index == -1:
				return None, speech_used
			print(index)
			return self.jumps[index], True

		elif motion == 'spin':
			if index == -1 and not speech_used:
				index = self.spin_speech(speech)
			if index == -1:
				return None, speech_used
			try:
				return self.spins[index-1], True
			except:
				return None, speech_used

		return None, speech_used

	def jump_speech(self, speech):
		print(speech)

		if 'axle' in speech or 'axel' in speech or 'paxil' in speech:
			return 0

		if 'salchow' in speech or 'socal' in speech or 'southco' in speech or 'falcao' in speech:
			return 1

		if speech in 'toe loop':
			return 2

		if speech in 'loop':
			return 3

		if 'flip' in speech or 'clip' in speech:
			return 4

		if 'lutz' in speech or "let's" in speech or 'lots' in speech:
			return 5

		return -1

	def spin_speech(self, speech):

		if 'combination' in speech:
			return 1

		if 'lay back' in speech or 'laid back' in speech or 'playback' in speech:
			return 2

		return -1




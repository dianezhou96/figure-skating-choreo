import sys
sys.path.append('..')

from common.core import *
from common.gfxutil import topleft_label, topright_label
import common.leaputil
import Leap

import numpy as np
import time

from moviepy.editor import AudioFileClip

from pprint import pprint
import pickle

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
		# self.last_time = time.time()

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
		# elif self.circle():
		#	return 'spin'
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
		# timestamp = time.time() - self.start_time
		left_fingers = self.left_hand.update(leap_frame)
		right_motion = self.right_hand.update(leap_frame)

		# print(right_motion)

		return left_fingers, right_motion

	def update(self):

		index, motion = self.recognize()

		if motion != None:
			print(index)

		if index == -1:
			return None

		if motion == 'jump':
			return self.jumps[index]

		elif motion == 'spin':
			try:
				return self.spins[index-1]
			except:
				pass


class MainWidget(BaseWidget):
	def __init__(self):
		super(MainWidget, self).__init__()

		self.gesture = Gesture()

		self.choreo = []

		try:
			music_name = sys.argv[2]
			music_file = '../data/' + music_name + '.wav'
		except:
			music_file = '../data/steiner.wav'
		music = AudioFileClip(music_file)
		self.total_duration = music.duration


		self.start_time = time.time()
		self.done = False

		self.info = topleft_label()
		self.add_widget(self.info)
		self.legend = topright_label()
		self.legend.text = \
			'Gesture Legend\n\n' +\
			'     Jumps: Swipe up with right hand\n' +\
			'     0 Axel\n' +\
			'     1 Salchow\n' +\
			'     2 Toeloop\n' +\
			'     3 Loop\n' +\
			'     4 Flip\n' +\
			'     5 Lutz\n\n' +\
			'     Spins: Make 5 circles with right finger\n' +\
			'     1 Combo\n' +\
			'     2 Layback'
		self.add_widget(self.legend)

	def on_update(self):

		timestamp = time.time() - self.start_time

		if timestamp < self.total_duration:
			element = self.gesture.update()

			if element != None:
				if element in self.gesture.jumps:
					self.choreo.append((max(0, timestamp-3), element))
				elif element in self.gesture.spins:
					self.choreo.append((max(0, timestamp-5), element))

				# self.choreo[max(0, timestamp-3)] = element

		elif not self.done:
			choreo_file = '../outputs/' + sys.argv[1]
			choreo_object = open(choreo_file, 'wb')
			pickle.dump(self.choreo, choreo_object)
			choreo_object.close()
			self.done = True

		self.update_text(timestamp)

	def update_text(self, timestamp):
		if self.done:
			self.info.text = 'Done\n\n'
		else:
			self.info.text = 'Time: %.1f' % timestamp + '\n\n'
		self.info.text += 'Current Gesture:\n'
		self.info.text += 'Left hand        Right hand\n'
		self.info.text += '%-25s' % \
			('None' if self.gesture.left_hand.num_fingers == -1 \
				else str(self.gesture.left_hand.num_fingers))
		self.info.text += self.gesture.right_hand.state + '\n\n'
		# self.info.text += '\n\n'
		self.info.text += 'Choreography:\n'
		self.info.text += 'Timestamp      Element\n'
		for timestamp, element in self.choreo:
			self.info.text += '%-25s' % ('%.1f' % (timestamp+3))
			self.info.text += element + '\n'
			# self.info.text += '\n'


start_time = time.time()
# m = Gesture(start_time)
# phrase = 1
run(MainWidget)
# music_file = '../data/steiner.wav'
# music = AudioFileClip(music_file)
# total_duration = music.duration
# while time.time() - start_time < total_duration:
# 	widget.on_update()

# choreo = m.get_choreo()
# choreo_file = 'testfile'
# choreo_object = open(choreo_file, 'wb')
# pickle.dump(choreo, choreo_object)
# choreo_object.close()
# pprint(choreo)



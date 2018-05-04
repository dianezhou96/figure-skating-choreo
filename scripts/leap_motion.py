import sys
sys.path.append('..')
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
		pass

	def update(self, leap_frame):
		if len(leap_frame.hands) == 1 and leap_frame.hands[0].is_left:
			return len(leap_frame.hands[0].fingers.extended())
		elif len(leap_frame.hands) == 2:
			if leap_frame.hands[0].is_left:
				return len(leap_frame.hands[0].fingers.extended())
			else:
				return len(leap_frame.hands[1].fingers.extended())
		return 0

class RightHand:
	def __init__(self):
		self.zpos = 5
		self.can_cross = False
		self.crossed_up = False
		self.threshold = 0.5
		self.last_time = time.time()

	def update(self, leap_frame):

		current_time = time.time()

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

		# print self.zpos
		# Update attributes
		if current_time - self.last_time > 1 or self.zpos == -1:
			self.reset(current_time)

		if self.zpos < self.threshold:
			crossed = not self.can_cross and self.crossed_up
			# if crossed:
			# 	print self.threshold
			self.can_cross = True
			self.crossed_up = False
			self.last_time = current_time
		elif self.zpos > self.threshold:
			if self.can_cross and not self.crossed_up:
				self.can_cross = False
				self.crossed_up = True
				self.last_time = current_time
			crossed = False

		if crossed:
			print('jump')
			return 'jump'
		# elif self.circle():
		#	return 'spin'
		else:
			return None


	def reset(self, current_time):
		self.can_cross = False
		self.crossed_up = False
		self.last_time = current_time




class Gesture:
	def __init__(self, start_time):
		self.leap = Leap.Controller()
		self.left_hand = LeftHand()
		self.right_hand = RightHand()

		self.choreo = {}
		self.start_time = start_time

		self.jumps = ['axel', 'salchow', 'loop', 'flip', 'lutz']
		self.spins = ['layback', 'death-drop', 'combo']



	def recognize(self):
		leap_frame = self.leap.frame()
		timestamp = time.time() - self.start_time
		left_fingers = self.left_hand.update(leap_frame)
		right_motion = self.right_hand.update(leap_frame)

		# print(right_motion)

		return left_fingers, right_motion, timestamp

	def on_update(self):


		index, motion, timestamp = self.recognize()
		# self.recognize()
		if motion != None:
			print(index)
		# print(index)

		if index == 0:
			return

		if motion == 'jump':
			try:
				self.choreo[timestamp-3] = self.jumps[index-1]
				print(self.jumps[index-1])
			except:
				pass
		elif motion == 'spin':
			try:
				self.choreo[timestamp-3] = self.spins[index-1]
			except:
				pass


	def get_choreo(self):
		return self.choreo

	# def pop_queue(self):
	# 	try:
	# 		return self.queue.pop(0)
	# 	except:
	# 		return None

start_time = time.time()
m = Gesture(start_time)
# phrase = 1
music_file = '../data/steiner.wav'
music = AudioFileClip(music_file)
total_duration = music.duration
while time.time() - start_time < total_duration:
	m.on_update()

choreo = m.get_choreo()
choreo_file = 'testfile'
choreo_object = open(choreo_file, 'wb')
pickle.dump(choreo, choreo_object)
choreo_object.close()
pprint(choreo)



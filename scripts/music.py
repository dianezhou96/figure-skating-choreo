import sys
sys.path.append('..')

from common.audio import *
from common.mixer import *
from common.wavegen import *
from common.wavesrc import *

class Music:
	def __init__(self, music_file):
		self.audio = Audio(2)
		self.mixer = Mixer()
		self.wavegen = WaveGenerator(WaveFile(music_file))
		self.wavegen.reset()
		self.mixer.add(self.wavegen)
		self.audio.set_generator(self.mixer)
		self.playing = False

	def update(self, speech, timestamp, used):

		if not used:

			used = False # whether timestamp changes due to speech

			# Process speech
			if 'pause' in speech:
				self.wavegen.pause()
				self.playing = False
				used = True

			elif 'play from' in speech:
				new_timestamp = self.get_time_from_speech(speech[10:])
				if isinstance(new_timestamp, int):
					timestamp = new_timestamp
					self.playing = self.play_from(timestamp)
					used = True

			elif 'go back' in speech:
				time_back = self.get_time_from_speech(speech[8:])
				if isinstance(time_back, int):
					timestamp = max(0, timestamp - time_back)
					self.playing = self.play_from(timestamp)
					used = True

			elif 'fast forward' in speech:
				time_forward = self.get_time_from_speech(speech[13:])
				if isinstance(time_forward, int):
					timestamp += time_forward
					self.playing = self.play_from(timestamp)
					used = True

			elif 'play' in speech:
				self.wavegen.play()
				self.playing = True
				used = True

			elif 'done' in speech or 'dawn' in speech:
				self.wavegen.reset()
				self.playing = False
				used = True

		# Update
		self.audio.on_update()
		return timestamp, used

	def play_from(self, timestamp):
		try:
			self.wavegen.play_from(int(timestamp * Audio.sample_rate))
			return True
		except:
			return self.playing

	def get_time_from_speech(self, speech):
		words = speech.split(' ')

		try:
			if 'second' in words[1]:
				return int(words[0])
		except:
			return None


		
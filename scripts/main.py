from gesture import *
from music import *
import pickle
from common.core import *

class MainWidget(BaseWidget):
	def __init__(self):
		super(MainWidget, self).__init__()

		self.gesture = Gesture()
		self.speech_filename = 'transcript'
		self.speech = ''
		self.speech_used = True
		self.last_speech_time = time.time()

		self.saved = False

		self.choreo = []

		music_name = sys.argv[2]
		music_file = '../data/' + music_name + '.wav'
		music = AudioFileClip(music_file)
		self.total_duration = music.duration

		self.audio = Music(music_file)

		self.last_time = time.time()
		self.timestamp = 0

		self.info = topleft_label()
		self.add_widget(self.info)
		self.legend = topright_label()
		self.legend.text = \
			'Gesture Legend\n' +\
			'     Jumps: Swipe up with right hand\n' +\
			'       0 Axel\n' +\
			'       1 Salchow\n' +\
			'       2 Toeloop\n' +\
			'       3 Loop\n' +\
			'       4 Flip\n' +\
			'       5 Lutz\n' +\
			'     Spins: Make 5 circles with right finger\n' +\
			'       1 Combo\n' +\
			'       2 Layback\n\n' +\
			'Voice Commands\n' +\
			'     Elements: Say name of element\n' +\
			'     Delete an element: "Delete element #"\n' +\
			'     Music:\n' +\
			'        "Play"\n' +\
			'        "Pause"\n' +\
			'        "Play from # seconds"\n' +\
			'        "Go back # seconds"\n' +\
			'        "Fast forward # seconds"\n' +\
			'     When finished: "Done" or spacebar\n' +\
			'          and close window'

		self.add_widget(self.legend)

	def edit_choreo(self):

		if self.speech_used:
			return

		speech = self.speech.split(' ')
		if speech[0] == 'delete':
			try:
				if speech[2] == 'one':
					index = 1
				else:
					index = int(speech[2])
				del self.choreo[index-1]
				self.speech_used = True
			except:
				pass

	def on_update(self):

		self.choreo = sorted(self.choreo, key = lambda x: x[0])

		current_time = time.time()
		if self.audio.playing:
			self.timestamp += current_time - self.last_time
		self.last_time = current_time

		self.update_speech()
		self.timestamp, self.speech_used = self.audio.update(self.speech, self.timestamp, self.speech_used)
		self.edit_choreo()

		if self.timestamp < self.total_duration:

			self.saved = False
			element, self.speech_used = self.gesture.update(self.speech, self.speech_used)

			if element != None:
				self.choreo.append((max(0, self.timestamp-3), element))


		if not self.audio.playing:
			choreo_file = '../outputs/' + sys.argv[1]
			choreo_object = open(choreo_file, 'wb')
			pickle.dump(self.choreo, choreo_object)
			choreo_object.close()
			self.saved = True

		self.update_text()

	def update_speech(self):
		current_time = time.time()
		try:
			speech_object = open(self.speech_filename, 'r')
			speech = pickle.load(speech_object)
			speech_object.close()
		except:
			speech = ''
		if len(speech) > 0:
			self.speech = speech
			self.speech_used = False
			self.last_speech_time = current_time
			speech_object = open(self.speech_filename, 'wb')
			pickle.dump('', speech_object)
			speech_object.close()
		elif current_time - self.last_speech_time > 5:
			self.speech = ''
			self.speech_used = True
			self.last_speech_time = current_time

	def update_text(self):
		self.info.text = 'Time: %.1f' % self.timestamp + '\n\n'
		self.info.text += 'Music Playing: ' + str(self.audio.playing) + '\n\n'
		self.info.text += 'Speech: ' + self.speech + '\n\n'
		self.info.text += 'Current Gesture:\n'
		self.info.text += 'Left hand        Right hand\n'
		self.info.text += '%-20s' % \
			('None' if self.gesture.left_hand.num_fingers == -1 \
				else str(self.gesture.left_hand.num_fingers))
		self.info.text += self.gesture.right_hand.state + '\n\n'
		self.info.text += 'Choreography:\n'
		self.info.text += 'Timestamp      Element\n'

		i = 1
		for timestamp, element in self.choreo:
			self.info.text += '%-25s' % (str(i) + '   ' + '%.1f' % (timestamp+3))
			self.info.text += element + '\n'
			i += 1

	def on_key_down(self, keycode, modifiers):
		if keycode[1] == 'spacebar':
			self.speech = 'done'
			self.speech_used = False


run(MainWidget)



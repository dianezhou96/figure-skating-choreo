from leap_motion import *
# from speech import *
import pickle
from common.core import *
from common.audio import *
from common.mixer import *
from common.wavegen import *
from common.wavesrc import *



class MainWidget(BaseWidget):
	def __init__(self):
		super(MainWidget, self).__init__()

		self.gesture = Gesture()
		self.speech_filename = 'transcript'
		self.speech = ''
		# Clock.schedule_once(self.speech.callback)

		self.choreo = []

		try:
			music_name = sys.argv[2]
			music_file = '../data/' + music_name + '.wav'
		except:
			music_file = '../data/steiner.wav'
		music = AudioFileClip(music_file)
		self.total_duration = music.duration

		self.audio = Audio(2)
		self.mixer = Mixer()
		self.mixer.add(WaveGenerator(WaveFile(music_file)))
		self.audio.set_generator(self.mixer)

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

		self.update_speech()
		self.audio.on_update()

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

	def update_speech(self):
		speech_object = open(self.speech_filename, 'r')
		speech = pickle.load(speech_object)
		speech_object.close()
		if len(speech) > 0:
			self.speech = speech
			speech_object = open(self.speech_filename, 'wb')
			pickle.dump('', speech_object)
			speech_object.close()

		# return speech

	def update_text(self, timestamp):
		if self.done:
			self.info.text = 'Done\n\n'
		else:
			self.info.text = 'Time: %.1f' % timestamp + '\n\n'
		self.info.text += 'Speech: '
		self.info.text += self.speech + '\n\n'
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


# m = Music('data/memory.wav')
# # while True:
# # 	m.play()
# # words = [0] * 100000 + [1]
# # playing = True
# # i = 0
# s = Speech()

# # next_word = 'hello'
# playing = False
# while 1:
# 	if playing:
# 		m.play()
# 	else:
# 		m.pause()
# 	next_word = s.recognize()
# 	if next_word == 'play':
# 		playing = True
# 	elif next_word == 'pause':
# 		playing = False
# 	elif next_word == 'stop':
# 		m.stop()
# 		break

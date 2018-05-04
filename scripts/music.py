import pyaudio
import wave

class Music:
	def __init__(self, file):
		self.file = file
		self.f = wave.open(self.file, 'r')
		self.p = pyaudio.PyAudio()
		self.chunk = 1024
		self.stream = self.p.open(format = self.p.get_format_from_width(self.f.getsampwidth()),  
                			 	  channels = self.f.getnchannels(),  
                			 	  rate = self.f.getframerate(),  
               				 	  output = True)
		self.data = self.f.readframes(self.chunk)
		# self.playing = False

	def start(self):
		self.stream.start_stream()

	def play(self):
		# self.playing = True
		# self.stream.start_stream()
		if self.data:
			self.stream.write(self.data)
			self.data = self.f.readframes(self.chunk)
		# else: # restart
		# 	self.f = wave.open(self.file, 'r')
		# 	self.data = self.f.readframes(self.chunk)
			

	def pause(self):
		# self.playing = False
		self.stream.stop_stream()

	def stop(self):
		self.stream.stop_stream()
		self.stream.close()
		self.p.terminate()

# def check(word=1):
# 	return bool(word)

m = Music('../data/steiner.wav')
m.start()
while m.data:
	m.play()
# words = [0] * 100000 + [1]
# playing = True
# i = 0 
# while m.data:
# 	if playing:
# 		m.play()
# 	if i < len(words):
# 		playing = check(words[i])
# 		i += 1
# 	print(i)
m.stop()
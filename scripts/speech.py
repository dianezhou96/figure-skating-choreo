import speech_recognition as sr
import time
from pprint import pprint

class Speech:
	def __init__(self):
		self.r = sr.Recognizer()
		self.choreo = {}
		self.start_time = time.time()

	def recognize(self):
		with sr.Microphone() as source:
			print('listening')
			audio = self.r.listen(source)
		try:
			# self.r.recognize_google(audio)
			phrase_time = time.time() - self.start_time
			phrase = self.r.recognize_google(audio)
			print(phrase)
			self.choreo[phrase_time] = phrase
			return phrase
			# self.queue.append(phrase)
		except sr.UnknownValueError:
			print("Google could not understand audio")
		except sr.RequestError as e:
		    print("Google error; {0}".format(e))

	def get_choreo(self):
		return self.choreo

	# def pop_queue(self):
	# 	try:
	# 		return self.queue.pop(0)
	# 	except:
	# 		return None

s = Speech()
phrase = 1
while phrase != 'stop':
	phrase = s.recognize()

choreo = s.get_queue()
pprint(choreo)

# choreo = [(u'jump', 4.565325021743774),
#  (u"spin", 8.527209997177124),
#  (u'', 29.021706104278564),
#  (u'Chomp Chomp Chomp', 42.37233209609985),
#  (u'Munch Munch Munch New York', 57.86052203178406),
#  (u'caterpillar', 68.8457179069519),
#  (u'cat', 75.79102301597595),
#  (u'meow', 81.95754313468933),
#  (u'stop', 87.49124002456665)]

# with open('choreo.txt', 'w') as f:
# 	for line in choreo:
# 		f.write(str(line[1]) + ' ' + line[0] + '\n')

# choreo = json.dump(choreo)
# with open('choreo.json', 'w') as f:
# 	f.write(choreo)

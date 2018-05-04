from music import Music
from speech import Speech




m = Music('data/memory.wav')
# while True:
# 	m.play()
# words = [0] * 100000 + [1]
# playing = True
# i = 0
s = Speech()

# next_word = 'hello'
playing = False
while 1:
	if playing:
		m.play()
	else:
		m.pause()
	next_word = s.recognize()
	if next_word == 'play':
		playing = True
	elif next_word == 'pause':
		playing = False
	elif next_word == 'stop':
		m.stop()
		break

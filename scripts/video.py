import sys
import imageio
imageio.plugins.ffmpeg.download()
from moviepy.editor import *
import pickle

def make_video(choreo_file, music_file, video_clips):

	# print video_clips
	# return

	choreo_object = open(choreo_file, 'r')
	choreo = pickle.load(choreo_object)
	choreo_object.close()
	# format: [ (timestamp, name),
	#			(timestamp, name) ]
	# choreo = [(1.0, 'layback'), (10.0, 'layback'), (30.0, 'combospin')]

	music = AudioFileClip(music_file)
	total_duration = music.duration
	# print(total_duration)

	index_time = 0
	last_time = 0
	clips = []

	# need last_time to be less than the total_duration
	while last_time < total_duration:

		if index_time < len(choreo):
			next_time, element = choreo[index_time]
		else:
			next_time = total_duration

		# need filler
		if next_time > last_time:
			duration = min(next_time - last_time, video_clips['filler'].duration)
			next_clip = video_clips['filler'].subclip(0, duration)

		# ready for next clip
		else:
			next_clip = video_clips[element]

			# check if there is another clip; this one needs to end before it
			try:
				next_next_time, _ = choreo[index_time+1]
			except:
				next_next_time = total_duration

			duration = min(next_next_time - next_time, next_clip.duration)
			next_clip = next_clip.subclip(0, duration)
			index_time += 1

		# update last_time and clips
		last_time += duration
		clips.append(next_clip)

	# Make final clip by concatenating and adding music
	final_clip = concatenate_videoclips(clips)
	music = music.set_duration(min(final_clip.duration, music.duration))
	final_clip = final_clip.set_audio(music)
	# final_clip = final_clip.resize((480,270))
	return final_clip

def make_clips(clip_files):
	clips = {}
	for clip in clip_files:
		clips[clip[8:-4]] = VideoFileClip(clip)
	return clips

choreo_file = '../outputs/' + sys.argv[1]
music_file = '../data/' + sys.argv[2] + '.wav'
filename = '../outputs/' + sys.argv[1] + '.mp4'
# choreo_file = 'name'
# music_file = '../data/steiner.wav'
# filename = '../outputs/name.mp4'
clip_names = ['filler', 'axel', 'salchow', 'toeloop', 'loop', 'flip', 'lutz', 'combospin', 'layback']
for i in range(len(clip_names)):
	clip_names[i] = '../data/' + clip_names[i] + '.mp4'
video_clips = make_clips(clip_names)
video = make_video(choreo_file, music_file, video_clips)
video.write_videofile(filename, fps=10, audio_codec="aac")
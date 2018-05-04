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
	# choreo = pickle.load(choreo_file)
	# format: { timestamp : name
	#			timestamp : name }
	times = sorted(choreo.keys())
	# times.sort() # times in order

	music = AudioFileClip(music_file)
	total_duration = music.duration
	# print(total_duration)

	index_time = 0
	last_time = 0
	clips = []

	# need last_time to be less than the total_duration
	# also need to have more elements left in choreo
	while last_time < total_duration:

		if index_time < len(times):
			next_time = times[index_time]
		else:
			next_time = total_duration

		# need filler
		if next_time > last_time:
			duration = min(next_time - last_time, video_clips['filler'].duration)
			next_clip = video_clips['filler'].subclip(0, duration)

		# ready for next clip
		else:
			next_clip = video_clips[choreo[next_time]]

			# check if there is another clip; this one needs to end before it
			try:
				next_next_time = times[index_time+1]
			except:
				next_next_time = float('inf')

			duration = min(next_next_time - next_time, next_clip.duration)
			next_clip = next_clip.subclip(0, duration)
			index_time += 1

		# update last_time and clips
		last_time += duration
		clips.append(next_clip)

	# Make final clip by concatenating and adding music
	final_clip = concatenate_videoclips(clips)
	music = music.set_duration(final_clip.duration)
	final_clip = final_clip.set_audio(music)
	# final_clip = final_clip.resize((480,270))
	return final_clip

def make_clips(clip_files):
	clips = {}
	for clip in clip_files:
		clips[clip[8:-4]] = VideoFileClip(clip)
	return clips

choreo_file = 'testfile'
music_file = '../data/steiner.wav'
filename = '../video.mp4'
clip_names = ['filler', 'axel', 'salchow', 'toeloop', 'loop', 'flip', 'lutz', 'combospin', 'layback']
for i in range(len(clip_names)):
	clip_names[i] = '../data/' + clip_names[i] + '.mp4'
video_clips = make_clips(clip_names)
video = make_video(choreo_file, music_file, video_clips)
video.write_videofile(filename, fps=10, audio_codec="aac")
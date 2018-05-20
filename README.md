# Figure Skating Choreography Off the Ice
Create and visualize figure skating choreography off the ice

## How to Use on Mac OS

### Setup
- Runs in Python 2.7
- ```pip install```
  - ```imageio```
  - ```moviepy```
  - ```pyaudio```
- Need to have Google Cloud Speech API credentials and ```GOOGLE_APPLICATION_CREDENTIALS``` variable set to path to JSON file with key (downloaded from Google Cloud account project)
- Uses Leap Motion
- Requires microphone (laptop microphone OK, prefer headphones due to music playing at same time)

### Usage
1. Put the music file (.wav) you want to use in the data folder, or use one provided
2. Navigate to scripts folder. In Terminal, execute: chmod u+x script.sh
3. Run ```./script.sh choreofilename audiofilename```
  - ```choreofilename``` can be any name you want 
  - ```audiofilename``` should be the name of the audio file you want, without the .wav extension
4. Create choreography! See below for how to do so, and the screen that pops up should also provide useful information. Note that speech recognition lasts only 65 seconds.
5. Say “done” or press the spacebar when done, then exit the window. The video should start rendering.
6. When the video is done rendering, find it in the outputs folder, and visualize the choreography you made!

### Creating Choreography

User uses voice commands to control what part of the music to play, as well as to edit elements.
- “Play” - play from last pause
- “Pause” - pause music
- “Play from # seconds” - play music from # seconds in
- “Go back # seconds” - rewind music by # seconds
- “Fast forward # seconds” - fast forward music by # seconds
- “Delete element #” - delete #-th element in the choreography

While music is playing, user does gestures over a Leap Motion that correspond to the elements desired, at the time in the music that the element should be done. There are two ways to do this:
- Two hands on Leap Motion
  - Right hand motion represents which type of element to do (jump or spin)
  - Left hand number of extended fingers represents which specific element to do (there are 6 jumps and 2 spins)
- One hand on Leap Motion, voice for specific element
  - Right hand motion represents which type of element to do (jump or spin)
  - Voice specifies specific element

During this time, the system records what part of the music the user does the gestures. After the user says “Done” or the spacebar is pressed, the system writes a file that lists timestamps and elements.

## Contents
- scripts - scripts Diane wrote or modified
  - script.sh - shell script; runs main.py and speech.py concurrently
  - main.py - main script that 
    - has the Kivy widget
    - displays information on screen
    - reads speech transcript from transcript pickle file
    - keeps the state of system 
    - writes choreography file to a file outputs folder
  - music.py - handles playing audio and processes speech to navigate to different times in the music
  - gesture.py - handles data from the Leap Motion and gesture recognition; also determines what the corresponding element is according to the gesture and speech
  - speech.py - handles speech recognition
    - modified from Google Cloud Speech sample script
    - writes transcript to transcript pickle file
  - video.py - stitches together videos from data folder based on choreography file in outputs folder
  - transcript - pickle file that speech.py writes and main.py reads
- common - scripts originally written by Eran Egozy (21M.385 - Interactive Music Systems) to handle audio playing, the Kivy framework, and Leap Motion functions. I added a function in gfxutil.py to have text on the right side of the screen
- data - input files
  - video files for stitching together videos (.mp4)
  - audio files for music (.wav)
- outputs - output file of the system from previous uses; for each use, there is a pickle file that has the choreography, and a video file (.mp4) of the same name

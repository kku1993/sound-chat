import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

import pyaudio
import time
import wave

CHUNK = 1024

def getFrames(f):
  wf = wave.open(f, 'rb')

  p = pyaudio.PyAudio()

  frames = []
  while True:
    data = wf.readframes(CHUNK)
    if data == '':
      break
    frames.append(data)

  wf.close()
  return frames

one = getFrames("one.wav")
zero = getFrames("zero.wav")
syn = getFrames("syn.wav")

p = pyaudio.PyAudio()
stream = p.open(format=16/2,
                channels=2,
                rate=44100,
                output=True)

for f in syn:
  stream.write(f)

for i in xrange(0, 8):
  if i % 2 == 0:
    for f in one:
      stream.write(f)
  else:
    for f in zero:
      stream.write(f)

stream.stop_stream()
stream.close()

p.terminate()

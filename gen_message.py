from config import *

import pyaudio
import time
import wave

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
stream = p.open(format=FORMAT/2,
                channels=CHANNELS,
                rate=RATE,
                output=True)

for f in syn:
  stream.write(f)

for i in xrange(0, 4):
  if i % 2 == 0:
    for f in one:
      stream.write(f)
  else:
    for f in zero:
      stream.write(f)

stream.stop_stream()
stream.close()

p.terminate()

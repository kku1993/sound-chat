from config import *

import pyaudio
import time
import wave
import random

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
noise = getFrames("noise.wav")

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT/2,
                channels=CHANNELS,
                rate=RATE,
                output=True)

def playNoise():
  for f in noise:
    stream.write(f)

for f in syn:
  stream.write(f)
playNoise()
# Fill in with blanks
# restFrames = int(RATE * WINDOW) % RATE
# stream.write(b'\x80' * restFrames)

for i in xrange(0, 16):
  b = random.randint(0, 1)
  print b

  if b == 1:
    for f in one:
      stream.write(f)
  else:
    for f in zero:
      stream.write(f)

  playNoise()

  # Fill in with blanks
  # restFrames = int(RATE * WINDOW) % RATE
  # stream.write(b'\x80' * restFrames)

stream.stop_stream()
stream.close()

p.terminate()

import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

import pyaudio
import math
import time
import wave
from itertools import izip

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

"""
# Generate audio
p = pyaudio.PyAudio()

volume = 1
frequency = 19000
sample_rate = RATE
duration = 7

n_samples = int(sample_rate * duration)
restframes = n_samples % sample_rate

s = lambda t: volume * math.sin(2 * math.pi * frequency * t / sample_rate)
samples = (int(s(t) * 0x7f + 0x80) for t in xrange(n_samples))

samples = ([x, x] for x in samples)
samples = [item for sublist in samples for item in sublist]

message = bytes(bytearray(samples))
print len(message)

# Fill the rest with silence.
message += (b'\x80' * restframes)

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(2)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(message)
wf.close()
p.terminate()
"""

# Playback
wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

data = wf.readframes(CHUNK)

while data != '':
  stream.write(data)
  data = wf.readframes(CHUNK)

stream.stop_stream()
stream.close()

p.terminate()

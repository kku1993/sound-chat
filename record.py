import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
  data = stream.read(CHUNK)
  frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

# Low pass filter
sound = np.fromstring("".join(frames), dtype=np.int16)
left, right = sound[0::2], sound[1::2]
lf, rf = np.fft.rfft(left), np.fft.rfft(right)

maxFreq = 0
maxCount = 0
for i in xrange(0, len(lf)):
  if lf[i] > maxCount:
    maxFreq = i
    maxCount = lf[i]
print maxFreq

# Plot
plt.figure(1)
"""
a = plt.subplot(211)
r = 2**16/2
a.set_ylim([-r, r])
a.set_xlabel('time [s]')
a.set_ylabel('sample value [-]')
x = np.arange(44100)/44100
plt.plot(x, left)
"""

b = plt.subplot(211)
b.set_xscale('log')
b.set_xlabel('frequency [Hz]')
b.set_ylabel('|amplitude|')
plt.plot(abs(lf))

lowpass = 600 # Remove lower frequencies.
highpass = 900 # Remove higher frequencies.

lf[:lowpass], rf[:lowpass] = 0, 0 # low pass filter (1)
#lf[55:66], rf[55:66] = 0, 0 # line noise filter (2)
lf[highpass:], rf[highpass:] = 0,0 # high pass filter (3)

# Inverse FFT to convert frequencies back to sound.
nl, nr = np.fft.irfft(lf), np.fft.irfft(rf) # (4)
ns = np.column_stack((nl,nr)).ravel().astype(np.int16)

c = plt.subplot(212)
c.set_xscale('log')
c.set_xlabel('frequency [Hz]')
c.set_ylabel('|amplitude|')
plt.plot(abs(lf))
plt.savefig('sample-graph.png')

# Output to wav file
"""
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
"""

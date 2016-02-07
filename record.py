from config import *
import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt


RECORD_SECONDS = 7

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16,
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
lf0, rf0 = np.fft.rfft(left), np.fft.rfft(right)
lf1, rf1 = np.fft.rfft(left), np.fft.rfft(right)
lSyn, rSyn = np.fft.rfft(left), np.fft.rfft(right)
#lf1, rf1 = list(lf0), list(rf0)
#lSyn, rSyn = list(lf0), list(rf0)

# Plot

def filterFreq(freq, graphNum, lf, rf):
  lowpass = freq*RECORD_SECONDS*0.95 # Remove lower frequencies.
  highpass = freq*RECORD_SECONDS*1.05 # Remove higher frequencies.

  lf[:lowpass], rf[:lowpass] = 0, 0 # low pass filter (1)
  #lf[55:66], rf[55:66] = 0, 0 # line noise filter (2)
  lf[highpass:], rf[highpass:] = 0,0 # high pass filter (3)

  # Inverse FFT to convert frequencies back to sound.
  nl, nr = np.fft.irfft(lf), np.fft.irfft(rf) # (4)
  ns = np.column_stack((nl,nr)).ravel().astype(np.int16)

  c = plt.subplot(graphNum)
  #c.set_xscale('log')
  #c.set_xlabel('frequency [Hz]')
  #c.set_ylabel('|amplitude|')
  #plt.plot(abs(lf))

  plt.plot(ns)
  return ns

plt.figure(1)
ab = filterFreq(SYN_FREQUENCY, 211, lSyn, rSyn)
plt.savefig('syn.png')

maxA = 0
index = 0
for i in xrange(0,len(ab)):
  if (abs(ab[i]) > maxA):
    maxA = abs(ab[i])
    index = i;

print "SYN Time: %d ms" % (index)

plt.figure(2)
ns0 = filterFreq(ZERO_FREQUENCY, 211, lf0, rf0)
ns1 = filterFreq(ONE_FREQUENCY, 212, lf1, rf1)
plt.savefig('ns.png')

result = []
timeIncrement = int(WINDOW*100000)
for i in xrange(index+timeIncrement,len(ns0), timeIncrement):
  sum0 = 1
  sum1 = 1
  for j in xrange(i, i+timeIncrement):
    if j >= len(ns0):
      break
    sum0 += abs(ns0[j])
    sum1 += abs(ns1[j])
  sum0 = sum0 / timeIncrement
  sum1 = sum1 / timeIncrement
  print "sum 0 is %d" % sum0
  print "sum 1 is %d" % sum1
  print "~~~~~~~~~~~"
  if (sum0 > sum1):
    result.append(0)
  else: 
    result.append(1)

print result

# Output to wav file
"""
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
"""

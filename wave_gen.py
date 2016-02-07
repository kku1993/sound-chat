# Generate wav files for ZERO, ONE, and SYN tones

import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

from pippi import dsp

def makeTone(numSec, freq, name):
  tone = dsp.tone(dsp.stf(numSec), freq=freq, amp=1) 
  dsp.write(tone, name)

makeTone(0.05, 500, "zero")
makeTone(0.05, 1000, "one")
makeTone(0.05, 10000, "syn")

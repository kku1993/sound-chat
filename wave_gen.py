# Generate wav files for ZERO, ONE, and SYN tones

from config import *

from pippi import dsp

def makeTone(numSec, freq, name):
  tone = dsp.tone(dsp.stf(numSec), freq=freq, amp=1) 
  dsp.write(tone, name)

makeTone(WINDOW, ZERO_FREQUENCY, "zero")
makeTone(WINDOW, ONE_FREQUENCY, "one")
makeTone(WINDOW, SYN_FREQUENCY, "syn")
makeTone(WINDOW, 50, "noise")

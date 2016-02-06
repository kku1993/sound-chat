import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

from pippi import dsp
import math

#out = dsp.tone(dsp.stf(0.05), freq=500, amp = 1)

ZERO = dsp.tone(dsp.stf(1), freq=50, amp=1)
ONE = dsp.tone(dsp.stf(1), freq=500, amp=1)

def f(i):
  if i % 2 == 0:
    return ONE
  return ZERO

#out = [ f(i) for i in xrange(0, 20) ]
#out = [ dsp.env(o, 'hann') for o in out ]
#out = reduce(dsp.add, out)

#out = dsp.tone(dsp.stf(5), freq=500, amp=0)
#for i in xrange(0, 5):
#  ONE = dsp.tone(dsp.stf(1), freq=500, amp=1, wavetype='hann',
#      phase=2 * math.pi * 500 * i)
#  env = dsp.env(ONE, 'hann')
#  dsp.add(out, ONE)

out = dsp.tone(dsp.stf(5), freq=500, amp=1)
out = dsp.amp(out, 0.1)
out = dsp.pad(out, dsp.stf(1), dsp.stf(5))

dsp.write(out, 'output')

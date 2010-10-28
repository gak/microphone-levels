#!/usr/bin/env python
from __future__ import division

import os
import pyaudio
import wave
import sys

chunk = 1024
FORMAT = pyaudio.paInt8
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 0.1
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                frames_per_buffer = chunk)

buffer = ''

while 1:
    data = stream.read(chunk)
    buffer += data
    if len(buffer) <= RATE:
        datachunk = buffer[:RATE]
        buffer = buffer[RATE:]
        # os.system('clear')
        numbers = [ord(a) for a in datachunk]
        vol = sum(numbers)
        print '%10i %.2f' % (vol, vol / (RATE)),
        print '-' * int(vol / RATE * 10)

#all = []
#for i in range(0, RATE / chunk * RECORD_SECONDS):
#    data = stream.read(chunk)
#    all.append(data)
#print "* done recording"



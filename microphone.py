#!/usr/bin/env python
from __future__ import division

import os
import pyaudio
import wave
import sys
import pyglet

class Microphone(pyglet.window.Window):

    def __init__(self):
        super(Microphone, self).__init__()
        self.label = pyglet.text.Label('Hello, world!')

        self.chunk = 1024
        FORMAT = pyaudio.paInt8
        self.channels = 1
        self.rate = 44100

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format = FORMAT,
            channels = self.channels,
            rate = self.rate,
            input = True,
            frames_per_buffer=self.chunk)

        self.buffer = ''

        pyglet.clock.schedule_interval(self.update, 0.001)

    def next_sample(self):
        while 1:
            try:
                data = self.stream.read(self.chunk)
            except IOError:
                continue
            self.buffer += data
            if len(self.buffer) <= self.rate:
                datachunk = self.buffer[:self.rate]
                self.buffer = self.buffer[self.rate:]
                numbers = [ord(a) for a in datachunk]
                vol = sum(numbers)
                print '%10i %.2f' % (vol, vol / (self.rate)),
                print '-' * int(vol / self.rate * 10)
                return numbers, vol

    def update(self, m):
        self.clear()
        data, vol = self.next_sample()
        self.label.text = str(vol)
        self.label.draw()
        pyglet.graphics.draw(int(len(data) / 2), pyglet.gl.GL_LINE_LOOP,
            ('v2i', data)
        )

if __name__ == '__main__':
    window = Microphone()
    pyglet.app.run()


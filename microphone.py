#!/usr/bin/env python
from __future__ import division

import os
import pyaudio
import wave
import sys
import pyglet
from pyglet.gl import *
from numpy import *
from numpy.fft import fft

class Microphone(pyglet.window.Window):

    def __init__(self, *args, **kw):
        super(Microphone, self).__init__(*args, **kw)
        self.num_samples = 512
        self.frames_per_buffer = self.num_samples
        self.format = pyaudio.paInt16
        self.channels = 1
        self.sampling_rate = 11025
        self.sampling_rate = 11025 * 4

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format = self.format,
            channels = self.channels,
            rate = self.sampling_rate,
            input = True,
            frames_per_buffer=self.frames_per_buffer)

        self.buffer = ''

        pyglet.clock.schedule_interval(self.update, 0.001)

    def read_fft(self):
        try:
            audio_data = fromstring(self.stream.read(self.num_samples),
                dtype=short)
        except IOError:
            return
        normalized_data = audio_data / 32768.0
        return fft(normalized_data)[1:1 + self.num_samples // 2]

    def update(self, m):
        data = self.read_fft()
        if data is None:
            return
        
        self.clear()

        if 0:
            data *= 100
            data += self.width / 2
            pyglet.graphics.draw(len(data) // 2, pyglet.gl.GL_LINE_LOOP,
                ('v2f', data)
            )

        else:
            graph = []
            w = 5
            glLineWidth(w)
            for s, value in enumerate(data):
                graph.append(s * w + w / 2)
                graph.append(0)
                graph.append(s * w + w / 2)
                graph.append(value * 100)
            pyglet.graphics.draw(len(graph) // 2, pyglet.gl.GL_LINES,
                ('v2f', graph))

if __name__ == '__main__':
    window = Microphone(width=2500, height=768)
    pyglet.app.run()


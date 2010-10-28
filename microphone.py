#!/usr/bin/env python -OO
from __future__ import division

import random
import colorsys
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

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format = self.format,
            channels = self.channels,
            rate = self.sampling_rate,
            input = True,
            frames_per_buffer=self.frames_per_buffer)

        self.buffer_w, self.buffer_h = self.width - 1, self.height - 1
        self.buffer_size = self.buffer_w * self.buffer_h
        self.screen_buffer = (GLuint * self.buffer_size)(0)
        pyglet.clock.schedule_interval(self.update, 1 / 60)

    def read_fft(self):
        try:
            audio_data = fromstring(self.stream.read(self.num_samples),
                dtype=short)
        except IOError:
            return
        normalized_data = audio_data / 32768.0
        return fft(normalized_data)[1:1 + self.num_samples // 2]

    def update(self, m):
        self.clear()

        data = None
        while data is None:
            data = self.read_fft()
        
        glDisable(GL_BLEND)
        glColor4f(1, 1, 1, 1)
        glRasterPos2i(0, 2)
        glDrawPixels(self.buffer_w, self.buffer_h, GL_RGBA, GL_BYTE, 
            self.screen_buffer)

        glColor4f(1, 1, 1, 0.5)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        graph = []
        colours = []
        w = 4
        glLineWidth(w)
        for s, value in enumerate(data):
            graph.append(s * w + w / 2)
            graph.append(0)
            graph.append(s * w + w / 2)
            # graph.append(1 + value * 10000 / self.num_samples)
            graph.append(2)
            v = float(value / 2)
            if v < 0:
                v = 0
            if v > .2:
                v = .2
            hue = colorsys.hls_to_rgb(v, .5, .5)
            colours += hue
            colours.append(.3 + v)
            colours += hue
            colours.append(.3 + v)
        pyglet.graphics.draw(len(graph) // 2, pyglet.gl.GL_LINES,
            ('v2f', graph),
            ('c4f', colours),
            )
        
        glReadPixels(0, 0, self.buffer_w, self.buffer_h, GL_RGBA, GL_BYTE, 
                self.screen_buffer)

if __name__ == '__main__':
    window = Microphone(width=1024, height=768)
    pyglet.app.run()


""" Record a few seconds of audio and save to a WAVE file. """

import logging
import sys
import wave
from itertools import izip
import pyaudio
import numpy as np

#PyAudio setup
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 96000
SAMPLES_PER_SECOND = 100

chunk_size = RATE / SAMPLES_PER_SECOND
seconds_per_sample = 1.0 / SAMPLES_PER_SECOND

#default frequency
BASE_FREQUENCY = 1010.0

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                frames_per_buffer = chunk_size)

def format_audio(chunk):
    """
    Create NumPy arrays of L/R channels from chunk
    """
    data = np.fromstring(chunk, dtype=np.short)
    ldata = data[0::2]
    rdata = data[1::2]
    return (ldata, rdata)

def argmax(array):
    """
    Stolen from http://www.daniel-lemire.com/blog/archives/2008/12/17/fast-argmax-in-python/

    The faster option he gives doesn't work with NumPy arrays.
    """
    return max(izip(array, xrange(len(array))))[1]

def get_freq(signal):
    """
    Given a PyAudio input chunk, determine the dominant frequency
    """
    #do the fft, this code adapted from
#http://stackoverflow.com/questions/6908540/pyaudio-how-to-tell-frequency-and-amplitude-while-recording
    p = 20*np.log10(np.abs(np.fft.rfft(signal)))
    f = np.linspace(0, RATE/2.0, len(p))
    offset = 1 # remove the first few entries in the fft
    #(first few entries are usually big but not what we're looking for)
    return f[argmax(p[offset:]) + offset]

def get_relative_velocity(chunk):
    """
    Returns the velocity of the record relative to the base velocity

    i.e. normal speed = 1.0
    reverse at normal speed = -1.0
    stopped = 0.0
    """
    lchunk, rchunk = format_audio(chunk)

    #only need one chunk for frequency
    freq = get_freq(lchunk)

    #determine direction
    argmax_l = argmax(lchunk[:chunk_size / 2])
    peak_offset = chunk_size / (seconds_per_sample * freq) / 4

    if rchunk[min(argmax_l + peak_offset, len(rchunk) - 1)] < 0:
        direction = 1
    else:
        direction = -1
    return round(direction * (freq / BASE_FREQUENCY), 1)

print "* recording"
#for i in range(0, RATE / chunk * RECORD_SECONDS):
while True:
    try:
        data = stream.read(chunk_size)
        velocity = get_relative_velocity(data)
        print ("velocity = %f" % velocity)
    except IOError:
        pass
        #logging.warning("audio error")

print "* done recording"

stream.close()
p.terminate()

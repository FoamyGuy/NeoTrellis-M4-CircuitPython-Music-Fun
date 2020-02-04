#!/usr/bin/python
# based on : www.daniweb.com/code/snippet263775.html
# Adapted from sample code in Stack Overflow answer: https://stackoverflow.com/a/33913403/507810
import math
import wave
import struct

# Audio will contain a long list of samples (i.e. floating point numbers describing the
# waveform).  If you were working with a very long sound you'd want to stream this to
# disk instead of buffering it all in memory list this.  But most sounds will fit in
# memory.
audio = []
sample_rate = 8000.0 # 8k sample rate for "low quality".
                     # 44.1 kHz sample rate for "HD"

TONE_FREQ = {
    'C3': 131, 'D3': 147, 'E3': 165, 'F3': 175, 'G3': 196, 'A3': 220, 'B3': 247,
    'C4': 262, 'D4': 294, 'E4': 330, 'F4': 349, 'G4': 392, 'A4': 440, 'B4': 494,
    'C5': 523, 'D5': 587, 'E5': 659, 'F5': 698, 'G5': 784, 'A5': 880, 'B5': 988,
    'Db3': 139, 'Eb3': 156, 'Gb3': 185, 'Db3': 208, 'Db3': 233,
}


def append_silence(duration_milliseconds=500):
    """
    Adding silence is easy - we add zeros to the end of our array
    """
    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    for x in range(int(num_samples)):
        audio.append(0.0)

    return


def append_sinewave(
        freq=440.0,
        duration_milliseconds=500,
        volume=1.0):
    """
    The sine wave generated here is the standard beep.  If you want something
    more aggresive you could try a square or saw tooth waveform.   Though there
    are some rather complicated issues with making high quality square and
    sawtooth waves...
    """

    global audio  # using global variables isn't cool.

    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    for x in range(int(num_samples)):
        audio.append(volume * math.sin(2 * math.pi * freq * (x / sample_rate)))

    return


def append_squarewave(
        freq=440.0,
        duration_milliseconds=500,
        volume=1.0):
    """

    """

    global audio  # using global variables isn't cool.

    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    for x in range(int(num_samples)):
        sine_val = volume * math.sin(2 * math.pi * freq * (x / sample_rate))
        if sine_val >= 0:
            audio.append(volume * 1)
        else:
            audio.append(-volume * 1)

    return


def append_sawtoothwave(
        freq=440.0,
        duration_milliseconds=500,
        volume=1.0):
    """

    """

    global audio  # using global variables isn't cool.

    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    for x in range(int(num_samples)):
        #sawtooth:
        P = 1 / freq
        sawtooth_val = volume * ((2/(P/2)) * ((P/2) - abs((x / sample_rate) % (2*(P/2) - P/2)))-1)
        audio.append(sawtooth_val)
    return


def append_trianglewave(
        freq=440.0,
        duration_milliseconds=500,
        volume=1.0):
    """

    """

    global audio  # using global variables isn't cool.

    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    for x in range(int(num_samples)):
        #tri_val = volume * ((x/sample_rate) % 1/freq)
        #tri_val = volume * (2 * abs(2*(((x/sample_rate)/(1/freq))-(((x/sample_rate)/(1/freq))+(1/2)))) - 1)
        tri_val = volume * (2 * 1 / math.pi) * math.asin(math.sin(2 * (math.pi / (1/freq)) * (x/sample_rate)))

        #sawtooth:
        #P = 1 / freq
        #tri_val = volume * ((2/(P/2)) * ((P/2) - abs((x / sample_rate) % (2*(P/2) - P/2)))-1)
        audio.append(tri_val)

    return


def save_wav(file_name):
    # Open up a wav file
    wav_file = wave.open(file_name, "w")

    # wav params
    nchannels = 2

    sampwidth = 2

    # 44100 is the industry standard sample rate - CD quality.  If you need to
    # save on file size you can adjust it downwards. The stanard for low quality
    # is 8000 or 8kHz.
    nframes = len(audio)
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))

    # WAV files here are using short, 16 bit, signed integers for the
    # sample size.  So we multiply the floating point data we have by 32767, the
    # maximum value for a short integer.  NOTE: It is theortically possible to
    # use the floating point -1.0 to 1.0 data directly in a WAV file but not
    # obvious how to do that using the wave module in python.
    for sample in audio:
        wav_file.writeframes(struct.pack('h', int(sample * 32767.0)))

    wav_file.close()

    return


for note in TONE_FREQ.keys():
    append_sinewave(freq=TONE_FREQ[note], volume=0.01)
    #append_squarewave(freq=TONE_FREQ[note], volume=0.01)
    #append_sawtoothwave(freq=TONE_FREQ[note], volume=0.01)
    #append_trianglewave(freq=TONE_FREQ[note], volume=0.01)
    print(audio)
    # append_silence(90)
    save_wav("%s.wav" % note)
    audio = []
    print("after save %s" % note)

import board
import audioio
import digitalio
import time
import adafruit_trellism4


trellis = adafruit_trellism4.TrellisM4Express()
trellis.pixels.brightness = 0.05
note_letters = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (46, 43, 95), (139, 0, 255)]
notes = {}
wave_dict = {3:"sine",4:"triangle",5:"sawtooth",6:"square"}

for octave in range(3,7):
    for note_letter in note_letters:
        cur_note = "%s%s" % (note_letter, octave)
        single_octave = "%s%s" % (note_letter, 4)
        notes[cur_note] = audioio.WaveFile(open("notes/%s/%s.wav" % (wave_dict[octave], single_octave), "rb"))

audio = audioio.AudioOut(left_channel=board.A0, right_channel=board.A1)
mixer = audioio.Mixer(voice_count=7, sample_rate=8000, channel_count=2, bits_per_sample=16, samples_signed=True)

audio.play(mixer)

for i, color in enumerate(colors):
    trellis.pixels[i,0] = color
    trellis.pixels[i,1] = color
    trellis.pixels[i,2] = color
    trellis.pixels[i,3] = color

prev_pressed = []
while True:
    #print(trellis.pressed_keys)
    cur_keys = trellis.pressed_keys
    if cur_keys != prev_pressed:
        print("different than last iter")
        pressed_key_xs = []
        if cur_keys != []:
            #audio.play(mixer)
            for key in cur_keys:

                if key[0] < len(note_letters):
                    note_for_key = "%s%s" % (note_letters[key[0]], key[1]+3)
                    if note_for_key in notes:
                        pressed_key_xs.append(key[0])
                        mixer.play(notes[note_for_key], voice=key[0], loop=True)
                        print("afterplay")

        if mixer.playing:
            for i in range(0,7):
                if i not in pressed_key_xs:
                    print("stopping %s" % i)
                    mixer.stop_voice(i)

    prev_pressed = cur_keys
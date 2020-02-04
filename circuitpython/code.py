import board
import audioio
import digitalio
import time
import adafruit_trellism4
trellis = adafruit_trellism4.TrellisM4Express()
trellis.pixels.brightness = 0.05
note_letters = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (56, 43, 105), (139, 0, 255)]
notes = {}

WAVE_TYPES = ["sine", "square", "sawtooth", "triangle"]

current_wave_type = "sine"
for wave_type in WAVE_TYPES:
    for octave in range(3,6):
        for note_letter in note_letters:
            cur_note = "%s%s" % (note_letter, octave)
            notes["%s%s" % (wave_type,cur_note)] = audioio.WaveFile(open("notes/%s/%s.wav" % (wave_type, cur_note), "rb"))
print(notes)
audio = audioio.AudioOut(left_channel=board.A0, right_channel=board.A1)
mixer = audioio.Mixer(voice_count=7, sample_rate=8000, channel_count=2, bits_per_sample=16, samples_signed=True)

audio.play(mixer)

for i, color in enumerate(colors):
    trellis.pixels[i,0] = color
    trellis.pixels[i,1] = color
    trellis.pixels[i,2] = color

prev_pressed = []
trellis.pixels[7,0] = (255,255,255)
while True:
    #print(trellis.pressed_keys)
    cur_keys = trellis.pressed_keys
    if cur_keys != prev_pressed:
        print("different than last iter")
        pressed_key_xs = []
        if cur_keys != []:
            #audio.play(mixer)
            print(cur_keys)
            for key in cur_keys:
                if key[0] < len(note_letters):
                    note_for_key = "%s%s" % (note_letters[key[0]], key[1]+3)
                    note_to_play = "%s%s" % (current_wave_type, note_for_key)
                    if note_to_play in notes:
                        pressed_key_xs.append(key[0])
                        mixer.play(notes[note_to_play], voice=key[0], loop=True)
                        print("afterplay")
                else:
                    print("last row")
                    current_wave_type = WAVE_TYPES[key[1]]
                    for y_pixel in range(0,4):
                        trellis.pixels[7,y_pixel] = (0,0,0)
                    trellis.pixels[7,key[1]] = (255,255,255)
        if mixer.playing:
            for i in range(0,7):
                if i not in pressed_key_xs:
                    print("stopping %s" % i)
                    mixer.stop_voice(i)

    prev_pressed = cur_keys
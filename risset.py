# coding=utf-8
import math
import pyaudio     #sudo apt-get install python-pyaudio
import time
p = pyaudio.PyAudio()

BITRATE = 16000     #number of frames per second/frameset.      

#generating wawes
def sines(bank, t):
  mix = 0
  for f in bank:
    mix += math.sin(2 * math.pi * f * t / BITRATE)
  return mix

# Перевод секунд в количество сэмплов
def sec(x):
  return BITRATE * x

def createGenerator():
    f = 96
    i1 = 0.03
    i2 = i1 * 2
    i3 = i1 * 3
    i4 = i1 * 4
    
    risset = []

    # Добавление 63 (9 * 7) частот в массив risset
    for i in [f, f + i1, f + i2, f + i3, f + i4, f - i1, f - i2, f - i3, f - i4]:
      for j in [i, 5 * i, 6 * i, 7 * i, 8 * i, 9 * i, 10 * i]:
        risset.append(j)
    t = 0
    while True:
        value = 0.01 * sines(risset, t)
        yield value
        t += 1

generator = createGenerator()


def callback(in_data, frame_count, time_info, status):
    print time_info
    out = ''
    for i in range(frame_count): #BYTES IN FRAME = 1024
        out += chr(int(generator.next()*127+128))
    return (out, pyaudio.paContinue)
 
stream = p.open(format=p.get_format_from_width(1),
                channels=1,
                rate=BITRATE,
                input=False,
                output=True,
                stream_callback=callback)
 
stream.start_stream()
 
while stream.is_active():
    time.sleep(0.1)
 
stream.stop_stream()
stream.close()
 
p.terminate()

import pyaudio
import numpy as np
import time
 
CHANNELS = 1
RATE = 48000
 
p = pyaudio.PyAudio()
 
rm_freq = 10.0
rm_phase = 0
 
def callback(in_data, frame_count, time_info, status):
    global rm_phase
    samples = np.fromstring(in_data, dtype=np.float32)
    out = np.zeros(len(samples), dtype=np.float32)
    for i in range(len(samples)):
        out[i] = samples[i] * np.sin(rm_phase)
        rm_phase += rm_freq / RATE * 2 * np.pi
    return (out.tostring(), pyaudio.paContinue)
 
stream = p.open(format=pyaudio.paFloat32,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                stream_callback=callback)
 
stream.start_stream()
 
while stream.is_active():
    time.sleep(0.1)
 
stream.stop_stream()
stream.close()
 
p.terminate()

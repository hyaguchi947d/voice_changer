#!/usr/bin/env python

import time
import numpy as np
import pyaudio
import pyworld as pw
import tkinter as tk
import functools

pa = pyaudio.PyAudio()

## please edit for your env.
input_device_index = 7
output_device_index = 0

rate = 48000
chunk = 1024 * 8
ch = 2

# frame_period = float(chunk) / float(rate)
# frame_period = pw.default_frame_period  # = 5.0
frame_period = 2.0


f_scale = 1.0
def change_f_scale(v):
    global f_scale
    f_scale = float(v)
    # print(f_scale)

sp_scale = 1.0
def change_sp_scale(v):
    global sp_scale
    sp_scale = float(v)
    # print(sp_scale)

def callback(in_data, frame_count, time_info, status):
    global f_scale
    global sp_scale
    # print(f_scale, sp_scale)
    np_data = np.fromstring(in_data, dtype=np.int16)
    np_stereo_data = np.reshape(np_data, (chunk, ch))
    np_l_data = np_stereo_data[:, 0]
    np_r_data = np_stereo_data[:, 1]
    np_lr_data = np_l_data / 2 + np_r_data / 2
    np_mono_data = np_lr_data.astype(np.float64)
    # print(np_mono_data.shape)

    of0, t = pw.dio(np_mono_data, rate, frame_period=frame_period)
    # print(of0.shape)
    # print(t.shape)
    f0 = pw.stonemask(np_mono_data, of0, t, rate)
    # print(f0.shape)
    sp = pw.cheaptrick(np_mono_data, f0, t, rate)
    # print(sp.shape)
    ap = pw.d4c(np_mono_data, f0, t, rate)
    # print(ap.shape)

    sp1 = np.zeros_like(sp)
    sp_rate = 1.0
    if sp_scale > 1.0:
        sp_rate = 1.0 / sp_scale
    else:
        sp_rate = sp_scale

    for f in range(sp.shape[1]):
        sp1[:, f] = sp[:, int(f * sp_rate)]    

    # np_synthesized = pw.synthesize(f0, sp, ap, rate, frame_period)
    np_synthesized = pw.synthesize(f0 * f_scale, sp1, ap, rate, frame_period)
    # print(np_synthesized.shape)
    # np_synthesized.shape != np_mono_data.shape

    np_out_data = np.empty((chunk, ch), dtype=np.float64)
    np_out_data[:, 0] = np_synthesized[:chunk]
    np_out_data[:, 1] = np_synthesized[:chunk]

    out_data = np_out_data.flatten().astype(np.int16).tostring()

    return (out_data, pyaudio.paContinue)


root = tk.Tk()
root.title("Voice Changer")
# frame = tk.Frame(root)
label_f_scale = tk.Label(root, text="f_scale")
label_f_scale.pack()
scale_f_scale = tk.Scale(root, orient=tk.HORIZONTAL,
    from_=0.5, to=2.0, resolution=0.1, length=200, command=change_f_scale)
scale_f_scale.set(1.0)
scale_f_scale.pack()
label_sp_scale = tk.Label(root, text="sp_scale")
label_sp_scale.pack()
scale_sp_scale = tk.Scale(root, orient=tk.HORIZONTAL,
    from_=0.5, to=2.0, resolution=0.1, length=200, command=change_sp_scale)
scale_sp_scale.set(1.0)
scale_sp_scale.pack()


stream = pa.open(
    format=pyaudio.paInt16,
    channels=ch,
    rate=rate,
    frames_per_buffer=chunk,
    input_device_index=input_device_index,
    output_device_index=output_device_index,
    input=True,
    output=True,
    stream_callback=callback)

try:
    root.mainloop()
    # while stream.is_active():
    #     time.sleep(0.1)
except KeyboardInterrupt:
    None
finally:
    stream.stop_stream()
    stream.close()

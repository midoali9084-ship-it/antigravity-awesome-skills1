"""Sanity-check a separation: reconstruction SNR and per-10s loudness of each stem.

Usage: python3 -I check.py <stems_dir>   (expects input.wav, vocals_only.wav, music_only.wav)
"""
import os, sys
import numpy as np
import soundfile as sf

d = sys.argv[1]
m, sr = sf.read(os.path.join(d, "input.wav"))
v, _ = sf.read(os.path.join(d, "vocals_only.wav"))
b, _ = sf.read(os.path.join(d, "music_only.wav"))
r = m - (v + b)
snr = 10 * np.log10((m ** 2).sum() / max((r ** 2).sum(), 1e-12))
rms = lambda x: 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-12)
print(f"duration {len(m)/sr:.1f}s | reconstruction SNR {snr:.1f} dB (>20 is good)")
print("t(s)  vocals_dB  music_dB   (vocals < -45 dB = instrumental section)")
step = 10 * sr
for i in range(len(m) // step):
    s = slice(i * step, (i + 1) * step)
    print(f"{i*10:4d}  {rms(v[s]):9.1f}  {rms(b[s]):8.1f}")

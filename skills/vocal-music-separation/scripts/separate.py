"""HTDemucs (ONNX) vocal / music separation.

Usage: python3 -I separate.py htdemucs.onnx input_44k_stereo.wav out_dir
Writes drums/bass/other/vocals.wav plus vocals_only.wav and music_only.wav.
"""
import math, sys, os, time
import numpy as np
import torch, torch.nn.functional as F
import soundfile as sf
import onnxruntime as ort

HL, NFFT, SR = 1024, 4096, 44100
SEG = int(7.8 * SR)  # 343980
SOURCES = ["drums", "bass", "other", "vocals"]


def pad1d(x, l, r):
    # reflect pad with small-input safety (as in demucs)
    L = x.shape[-1]
    mx = max(l, r)
    if L <= mx:
        extra = mx - L + 1
        er = min(r, extra); el = extra - er
        x = F.pad(x, (el, er)); l -= el; r -= er
    return F.pad(x, (l, r), mode="reflect")


def spec(x):
    L = x.shape[-1]
    le = math.ceil(L / HL)
    pad = HL // 2 * 3
    x = pad1d(x, pad, pad + le * HL - L)
    b, c, n = x.shape
    z = torch.stft(x.reshape(-1, n), NFFT, HL, window=torch.hann_window(NFFT), win_length=NFFT,
                   normalized=True, center=True, return_complex=True, pad_mode="reflect")
    z = z.view(b, c, *z.shape[-2:])[..., :-1, :]
    return z[..., 2:2 + le]


def magnitude(z):
    b, c, fr, t = z.shape
    m = torch.view_as_real(z).permute(0, 1, 4, 2, 3)
    return m.reshape(b, c * 2, fr, t)


def ispec(z, length):
    z = F.pad(z, (0, 0, 0, 1))
    z = F.pad(z, (2, 2))
    pad = HL // 2 * 3
    le = HL * math.ceil(length / HL) + 2 * pad
    *other, fr, t = z.shape
    x = torch.istft(z.reshape(-1, fr, t), NFFT, HL, window=torch.hann_window(NFFT), win_length=NFFT,
                    normalized=True, length=le, center=True)
    x = x.view(*other, -1)
    return x[..., pad:pad + length]


def infer(sess, chunk):
    # chunk: [1, 2, SEG] already padded
    z = spec(chunk)
    mag = magnitude(z).numpy().astype(np.float32)
    outX, outXt = sess.run(None, {sess.get_inputs()[0].name: chunk.numpy().astype(np.float32),
                                 sess.get_inputs()[1].name: mag})
    m = torch.from_numpy(outX)  # [1,4,4,Fr,T]
    b, s, c, fr, t = m.shape
    m = m.view(b, s, c // 2, 2, fr, t).permute(0, 1, 2, 4, 5, 3).contiguous()
    zout = torch.view_as_complex(m)
    return torch.from_numpy(outXt) + ispec(zout, SEG)


def main(model, inp, out_dir):
    wav, sr = sf.read(inp, dtype="float32", always_2d=True)
    assert sr == SR, sr
    wav = torch.from_numpy(wav.T.copy())  # [2, N]
    if wav.shape[0] == 1:
        wav = wav.repeat(2, 1)
    ref = wav.mean(0)
    mean, std = ref.mean(), ref.std()
    mix = ((wav - mean) / std)[None]
    N = mix.shape[-1]

    so = ort.SessionOptions(); so.intra_op_num_threads = os.cpu_count()
    sess = ort.InferenceSession(model, so, providers=["CPUExecutionProvider"])

    stride = int(0.75 * SEG)
    w = torch.cat([torch.arange(1, SEG // 2 + 2), torch.arange(SEG - SEG // 2 - 1, 0, -1)]).float()
    w = w / w.max()
    out = torch.zeros(1, 4, 2, N); sw = torch.zeros(N)
    total = math.ceil(N / stride); t0 = time.time()
    for i, off in enumerate(range(0, N, stride)):
        length = min(SEG, N - off)
        delta = SEG - length
        start = off - delta // 2; end = start + SEG
        cs, ce = max(0, start), min(N, end)
        chunk = F.pad(mix[..., cs:ce], (cs - start, end - ce))
        y = infer(sess, chunk)
        d = SEG - length; y = y[..., d // 2: d // 2 + length]
        out[..., off:off + length] += w[:length] * y
        sw[off:off + length] += w[:length]
        print(f"chunk {i+1}/{total}  {time.time()-t0:.0f}s", flush=True)
    out = out / sw
    out = out * std + mean
    out = out[0]
    os.makedirs(out_dir, exist_ok=True)
    for k, name in enumerate(SOURCES):
        sf.write(os.path.join(out_dir, f"{name}.wav"), out[k].T.numpy(), SR)
    vocals = out[3]
    music = out[0] + out[1] + out[2]
    sf.write(os.path.join(out_dir, "vocals_only.wav"), vocals.T.numpy(), SR)
    sf.write(os.path.join(out_dir, "music_only.wav"), music.T.numpy(), SR)
    print("done")


if __name__ == "__main__":
    main(*sys.argv[1:4])

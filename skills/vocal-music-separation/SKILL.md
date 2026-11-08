---
name: vocal-music-separation
description: "Use when the user asks to separate, isolate or remove vocals from music (عزل/فصل الصوت عن الموسيقى, karaoke, acapella, instrumental) in an audio file."
category: content
risk: safe
source: self
tags: "[audio, music, vocals, stem-separation, demucs, karaoke, acapella]"
date_added: "2026-11-08"
---

# Vocal / Music Separation (عزل الصوت عن الموسيقى)

Splits a song or recording into **vocals only** and **music only** (plus drums / bass / other stems)
with Meta's **HTDemucs** model, run locally on CPU through ONNX Runtime. No API key, no GPU.
About 30 s of processing per minute of audio on a 4-core machine.

## When to Use

- "اعزل الصوت عن الموسيقى" / "افصل الصوت عن الموسيقى" / "شيل الموسيقى" / "أريد الصوت بدون موسيقى"
- "Remove the vocals", "make a karaoke / instrumental version", "extract the acapella", "split into stems"
- Any audio or video file (MP3, WAV, M4A, FLAC, OGG, MP4…) where speech or singing must be separated from background music.

## Workflow

1. **Run the pipeline** on every file the user gave (multiple files in one call are fine).
   Output into the scratchpad (or a directory the user names):

   ```bash
   bash skills/vocal-music-separation/scripts/run.sh "<OUT_DIR>" "/path/to/song1.mp3" "/path/to/song2.mp3"
   ```

   The script installs `torch onnxruntime soundfile numpy` from PyPI if missing, downloads and
   caches the HTDemucs weights (from the npm registry, SHA-256 verified), converts to 44.1 kHz
   stereo, separates, encodes MP3 192k, and prints a quality check.
   Use a Bash timeout of ~10 min; a 4-minute song takes about 2 min.

2. **Read the quality check** it prints:
   - `reconstruction SNR` above ~20 dB → vocals + music add back to the original (good).
   - 10-second rows with vocals below about -45 dB are instrumental sections; if the user's
     song has an instrumental intro, the vocals track should be silent there.
   - If vocals are much quieter than the music throughout, warn that faint music bleed may remain.

3. **Deliver** `<OUT_DIR>/<name>/vocals.mp3` and `<OUT_DIR>/<name>/music.mp3` (SendUserFile when
   available), give full absolute paths, and mention that `stems/` also holds `drums.wav`,
   `bass.wav`, `other.wav`, `vocals.wav` if they want finer stems. Reply in the user's language.
   Be honest that the check is numeric — you did not listen to the result.

## Examples

```bash
# One file
bash skills/vocal-music-separation/scripts/run.sh /tmp/out "song.mp3"
# -> /tmp/out/song/vocals.mp3, /tmp/out/song/music.mp3, /tmp/out/song/stems/*.wav

# Only the Python step, on an already 44.1 kHz stereo WAV
python3 -I skills/vocal-music-separation/scripts/separate.py ~/.cache/vocal-music-separation/htdemucs.onnx in.wav out_stems
```

## Implementation Notes

- `scripts/separate.py` is a self-contained Python port of HTDemucs inference: STFT/iSTFT with
  `torch.stft`, 7.8 s segments with 25 % triangular-weighted overlap, mix normalisation, and the
  ONNX graph (`input` waveform + magnitude spectrogram → 4 stems).
- Weights come from the `htdemucs.onnx` file in the npm package `demucs@1.0.0`. Only that data
  file is extracted; the package's JavaScript is never executed.
- Why not `pip install demucs` / `audio-separator`? Their weights are fetched from
  `dl.fbaipublicfiles.com` or GitHub releases, which sandboxed cloud sessions often block.
  If those hosts are reachable, `python3 -m demucs --two-stems=vocals -n htdemucs_ft` is a fine alternative.

## Limitations

- Weights are derived from Meta's Demucs release and are for **personal and research use only**.
- Model is the base `htdemucs` (not `htdemucs_ft`/Roformer); very quiet or heavily reverbed vocals may
  keep slight music bleed, and backing vocals land in the vocals track.
- CPU only; long files (>15 min) need more RAM (~1 GB per 5 min of audio) and time.
- Needs `ffmpeg`, Python 3.10+, and network access to PyPI and registry.npmjs.org on first run.

#!/usr/bin/env bash
# Separate vocals from music in one or more audio files using HTDemucs (ONNX, CPU).
# Usage: run.sh <output_dir> <audio_file> [audio_file ...]
# Output per file: <output_dir>/<name>/{vocals.mp3,music.mp3} + stems/*.wav
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_ROOT="${1:?usage: run.sh <output_dir> <audio_file> [...]}"; shift
[ "$#" -ge 1 ] || { echo "no input files" >&2; exit 1; }

CACHE="${VMS_CACHE:-$HOME/.cache/vocal-music-separation}"
MODEL="$CACHE/htdemucs.onnx"
# Weights are taken from the npm "demucs" package tarball (data only; its JS code is never run).
TARBALL_URL="https://registry.npmjs.org/demucs/-/demucs-1.0.0.tgz"
TARBALL_SHA256="83aadd00d48cd2a0c2e81e2a35616f4fa41a41f5c07efcc4a5c1959377b4ec42"
MODEL_SHA256="da9e5101ee0804d04933974b59d8aae9c862e80e14f2f24e7c74cae76bdbe748"

# 1. Dependencies
command -v ffmpeg >/dev/null || { echo "ffmpeg is required (apt-get install -y ffmpeg)" >&2; exit 1; }
python3 -I -c "import torch, onnxruntime, soundfile, numpy" 2>/dev/null || \
  pip install -q torch onnxruntime soundfile numpy

# 2. Model weights (cached)
if [ ! -f "$MODEL" ] || ! echo "$MODEL_SHA256  $MODEL" | sha256sum -c --status; then
  mkdir -p "$CACHE/dl"
  curl -sSL -o "$CACHE/dl/demucs.tgz" "$TARBALL_URL"
  echo "$TARBALL_SHA256  $CACHE/dl/demucs.tgz" | sha256sum -c --status || { echo "tarball checksum mismatch" >&2; exit 1; }
  tar -xzf "$CACHE/dl/demucs.tgz" -C "$CACHE/dl" package/htdemucs.onnx
  mv "$CACHE/dl/package/htdemucs.onnx" "$MODEL"
  rm -rf "$CACHE/dl"
  echo "$MODEL_SHA256  $MODEL" | sha256sum -c --status || { echo "model checksum mismatch" >&2; exit 1; }
fi

# 3. Separate each file
for IN in "$@"; do
  NAME="$(basename "${IN%.*}")"
  OUT="$OUT_ROOT/$NAME"
  mkdir -p "$OUT/stems"
  echo "== $IN"
  ffmpeg -v error -y -i "$IN" -ar 44100 -ac 2 "$OUT/stems/input.wav"
  python3 -I "$SCRIPT_DIR/separate.py" "$MODEL" "$OUT/stems/input.wav" "$OUT/stems"
  ffmpeg -v error -y -i "$OUT/stems/vocals_only.wav" -b:a 192k "$OUT/vocals.mp3"
  ffmpeg -v error -y -i "$OUT/stems/music_only.wav"  -b:a 192k "$OUT/music.mp3"
  python3 -I "$SCRIPT_DIR/check.py" "$OUT/stems"
  echo "-> $OUT/vocals.mp3"
  echo "-> $OUT/music.mp3"
done

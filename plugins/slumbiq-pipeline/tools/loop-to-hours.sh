#!/bin/bash
# Slumbiq Loop Extender (crossfade method)
# Loops a short clip into an N-hour video using soft crossfades between iterations.
# Motion stays forward, loop points are dissolved.
#
# Usage:
#   loop-to-hours.sh <input.mp4> <output.mp4> <hours>

set -e

INPUT="$1"
OUTPUT="$2"
HOURS="${3:-8}"
FADE_SECONDS=2

if [ -z "$INPUT" ] || [ -z "$OUTPUT" ]; then
  echo "Usage: $0 <input.mp4> <output.mp4> <hours>"
  exit 1
fi

if [ ! -f "$INPUT" ]; then
  echo "Error: Input file not found: $INPUT"
  exit 1
fi

TARGET_SECONDS=$((HOURS * 3600))
TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

CLIP_SECONDS=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$INPUT" | cut -d. -f1)

echo "=== Slumbiq Loop Extender (Crossfade) ==="
echo "Input: $INPUT (${CLIP_SECONDS}s)"
echo "Output: $OUTPUT"
echo "Target: ${HOURS}h"
echo "Crossfade: ${FADE_SECONDS}s per loop"
echo ""

NET_PER_LOOP=$((CLIP_SECONDS - FADE_SECONDS))
LOOPS=$((TARGET_SECONDS / NET_PER_LOOP + 2))

echo "[1/2] Building seamless loop unit (forward + crossfade tail)..."

ffmpeg -y -hide_banner -loglevel error \
  -i "$INPUT" -i "$INPUT" \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=${FADE_SECONDS}:offset=$((CLIP_SECONDS - FADE_SECONDS))[v]" \
  -map "[v]" \
  -c:v libx264 -preset fast -crf 22 -pix_fmt yuv420p \
  "$TMPDIR/loop_unit.mp4"

UNIT_SECONDS=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$TMPDIR/loop_unit.mp4" | cut -d. -f1)
UNIT_LOOPS=$((TARGET_SECONDS / UNIT_SECONDS + 1))

echo "    Loop unit: ${UNIT_SECONDS}s, will repeat ${UNIT_LOOPS}x"
echo ""
echo "[2/2] Extending and encoding final ${HOURS}h video..."

ffmpeg -y -hide_banner -loglevel warning \
  -stream_loop $((UNIT_LOOPS - 1)) \
  -i "$TMPDIR/loop_unit.mp4" \
  -t "$TARGET_SECONDS" \
  -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p \
  -movflags +faststart \
  "$OUTPUT"

FINAL_SIZE=$(ls -lh "$OUTPUT" | awk '{print $5}')
echo ""
echo "=== DONE ==="
echo "Output: $OUTPUT ($FINAL_SIZE)"
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUTPUT" | awk '{printf "Duration: %.0fs (%.2fh)\n", $1, $1/3600}'

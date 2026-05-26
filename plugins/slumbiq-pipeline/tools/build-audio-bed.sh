#!/bin/bash
# Slumbiq Audio Bed Builder
# Loops + mixes two audio sources into an N-hour bed.
#
# Usage:
#   build-audio-bed.sh <foundation.wav> <atmosphere.wav> <output.wav> <hours>

set -e

FOUNDATION="$1"
ATMOSPHERE="$2"
OUTPUT="$3"
HOURS="${4:-8}"

if [ -z "$FOUNDATION" ] || [ -z "$ATMOSPHERE" ] || [ -z "$OUTPUT" ]; then
  echo "Usage: $0 <foundation.wav> <atmosphere.wav> <output.wav> <hours>"
  exit 1
fi

TARGET_SECONDS=$((HOURS * 3600))

echo "=== Slumbiq Audio Bed Builder ==="
echo "Foundation: $FOUNDATION (70% volume)"
echo "Atmosphere: $ATMOSPHERE (25% volume)"
echo "Output: $OUTPUT"
echo "Duration: ${HOURS}h (${TARGET_SECONDS}s)"
echo ""

ffmpeg -y -hide_banner -loglevel warning \
  -stream_loop -1 -i "$FOUNDATION" \
  -stream_loop -1 -i "$ATMOSPHERE" \
  -filter_complex "[0:a]volume=0.70[a0];[1:a]volume=0.25[a1];[a0][a1]amix=inputs=2:duration=first:dropout_transition=0[aout]" \
  -map "[aout]" \
  -t "$TARGET_SECONDS" \
  -c:a aac -b:a 192k \
  "$OUTPUT"

FINAL_SIZE=$(ls -lh "$OUTPUT" | awk '{print $5}')
echo ""
echo "=== DONE ==="
echo "Output: $OUTPUT ($FINAL_SIZE)"

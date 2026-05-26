#!/bin/bash
# Slumbiq Final Video Assembler
# Combines a stitched scene master with an audio bed into a YouTube-ready N-hour video.
#
# Usage:
#   assemble-video.sh <visual-master.mp4> <audio-bed.aac> <output.mp4> <hours>

set -e

VIDEO="$1"
AUDIO="$2"
OUTPUT="$3"
HOURS="${4:-8}"

if [ -z "$VIDEO" ] || [ -z "$AUDIO" ] || [ -z "$OUTPUT" ]; then
  echo "Usage: $0 <visual-master.mp4> <audio-bed.aac> <output.mp4> <hours>"
  exit 1
fi

TARGET_SECONDS=$((HOURS * 3600))
TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

VIDEO_SECONDS=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$VIDEO" | cut -d. -f1)
VIDEO_LOOPS=$((TARGET_SECONDS / VIDEO_SECONDS + 1))

echo "=== Slumbiq Final Video Assembler ==="
echo "Visual: $VIDEO (${VIDEO_SECONDS}s, will loop ${VIDEO_LOOPS}x)"
echo "Audio: $AUDIO"
echo "Output: $OUTPUT"
echo "Duration: ${HOURS}h (${TARGET_SECONDS}s)"
echo ""

echo "[1/2] Looping visual to ${HOURS}h..."
ffmpeg -y -hide_banner -loglevel warning \
  -stream_loop $((VIDEO_LOOPS - 1)) -i "$VIDEO" \
  -t "$TARGET_SECONDS" \
  -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p \
  -movflags +faststart \
  -an \
  "$TMPDIR/video_extended.mp4"

echo ""
echo "[2/2] Combining video + audio into final output..."
ffmpeg -y -hide_banner -loglevel warning \
  -i "$TMPDIR/video_extended.mp4" \
  -i "$AUDIO" \
  -map 0:v -map 1:a \
  -c:v copy \
  -c:a aac -b:a 192k \
  -shortest \
  -movflags +faststart \
  "$OUTPUT"

FINAL_SIZE=$(ls -lh "$OUTPUT" | awk '{print $5}')
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUTPUT" | awk '{printf "%.2fh", $1/3600}')
echo ""
echo "=== DONE ==="
echo "Output: $OUTPUT"
echo "Size: $FINAL_SIZE"
echo "Duration: $DURATION"

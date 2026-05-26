#!/bin/bash
# Slumbiq Scene Stitcher
# Stitches a scene's 5 variants into one 46-second loop-friendly master.
#
# Usage:
#   stitch-scene.sh <scene-name> [output-dir]
#
# Example:
#   stitch-scene.sh wet-street
#   stitch-scene.sh hearth-heart ~/slumbiq-masters

set -e

SCENE="$1"
OUTPUT_DIR="${2:-$HOME/slumbiq-tests/scene-library}"
SOURCE_DIR="$HOME/slumbiq-tests/scene-library"

if [ -z "$SCENE" ]; then
  echo "Usage: $0 <scene-name> [output-dir]"
  echo "Example: $0 wet-street"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

V1="$SOURCE_DIR/${SCENE}.mp4"
V2="$SOURCE_DIR/${SCENE}-v2.mp4"
V3="$SOURCE_DIR/${SCENE}-v3.mp4"
V4="$SOURCE_DIR/${SCENE}-v4.mp4"
V5="$SOURCE_DIR/${SCENE}-v5.mp4"

for f in "$V1" "$V2" "$V3" "$V4" "$V5"; do
  if [ ! -f "$f" ]; then
    echo "ERROR: Missing variant: $f"
    exit 1
  fi
done

OUTPUT="$OUTPUT_DIR/${SCENE}-master.mp4"

echo "=== Slumbiq Scene Stitcher ==="
echo "Scene: $SCENE"
echo "Output: $OUTPUT"
echo ""

ffmpeg -y -hide_banner -loglevel warning \
  -i "$V1" -i "$V2" -i "$V3" -i "$V4" -i "$V5" \
  -filter_complex "\
    [0:v][1:v]xfade=transition=fade:duration=1:offset=9[v01];\
    [v01][2:v]xfade=transition=fade:duration=1:offset=18[v012];\
    [v012][3:v]xfade=transition=fade:duration=1:offset=27[v0123];\
    [v0123][4:v]xfade=transition=fade:duration=1:offset=36[v01234];\
    [v01234][0:v]xfade=transition=fade:duration=1:offset=45[vfinal]" \
  -map "[vfinal]" \
  -c:v libx264 -preset medium -crf 22 -pix_fmt yuv420p \
  -movflags +faststart \
  "$OUTPUT"

FINAL_SIZE=$(ls -lh "$OUTPUT" | awk '{print $5}')
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUTPUT" | cut -d. -f1)
echo ""
echo "=== DONE ==="
echo "Output: $OUTPUT ($FINAL_SIZE, ${DURATION}s)"

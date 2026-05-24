#!/bin/bash
# Slumbiq Carousel Check - silent if no pending markers
# Outputs work needed signal only if uploaded videos need carousels

MARKERS_DIR="/Users/moen/.openclaw/workspace/markers/carousel"
LOG="/Users/moen/.openclaw/workspace/HEARTBEAT"

# Ensure markers directory exists
mkdir -p "$MARKERS_DIR"

# Count pending markers (files ending in .pending.json)
PENDING=$(find "$MARKERS_DIR" -maxdepth 1 -name "*.pending.json" -type f 2>/dev/null | wc -l | tr -d ' ')

echo "$(date '+%Y-%m-%d %H:%M') Slumbiq carousel check: $PENDING markers pending" >> "$LOG"

# If no pending markers, silent exit
if [ "$PENDING" -eq 0 ]; then
    exit 0
fi

# Output signal for main session to act
echo "SLUMBIQ_CAROUSEL_WORK_NEEDED: $PENDING markers pending in $MARKERS_DIR"

# List the pending markers so the main session knows what to process
find "$MARKERS_DIR" -maxdepth 1 -name "*.pending.json" -type f 2>/dev/null | while read -r marker; do
    video_id=$(basename "$marker" .pending.json)
    echo "  - $video_id ($marker)"
done

exit 0

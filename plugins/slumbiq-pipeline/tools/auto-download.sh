#!/bin/bash
cd ~/slumbiq-tests/scene-library
echo "=== $(date) ==="
DOWNLOADED=0
while IFS='|' read -r name req; do
  if [ ! -f "./${name}.mp4" ]; then
    genmedia status bytedance/seedance-2.0/fast/text-to-video "$req" --download "./${name}.mp4" --json > /dev/null 2>&1
    if [ -f "./${name}.mp4" ]; then
      echo "OK: ${name}.mp4"
      DOWNLOADED=$((DOWNLOADED + 1))
    fi
  fi
done < request_ids.txt
echo "Downloaded ${DOWNLOADED} new file(s). Library: $(ls *.mp4 | wc -l) total."

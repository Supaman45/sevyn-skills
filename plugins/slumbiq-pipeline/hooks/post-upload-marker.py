"""
Post-upload hook for Slumbiq video uploads.

Writes a pending marker file when a video finishes uploading to YouTube.
The carousel pipeline picks up these markers and processes them.

Called at the end of each slumbiq_upload_sl00X.py script:

    import subprocess
    subprocess.run([
        "python3",
        "/Users/moen/.claude/plugins/marketplaces/sevyn-skills/plugins/slumbiq-pipeline/hooks/post-upload-marker.py",
        "--video-id", "SL-001",
        "--video-url", uploaded_video_url,
        "--video-title", TITLE,
        "--video-path", VIDEO_PATH,
        "--duration-hours", "8",
        "--theme", "rain_car_roof",
        "--script-summary", "Eight hours of rain on a car rooftop for deep sleep.",
    ])
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

MARKERS_DIR = Path.home() / ".openclaw" / "workspace" / "markers" / "carousel"
SLUMBIQ_RENDERS = Path("/Volumes/ClawDrive/renders/slumbiq")


def find_thumbnail(video_id: str) -> str:
    """Find the final thumbnail for a video ID, falling back to raw."""
    sid = video_id.lower().replace("-", "")
    candidates = [
        SLUMBIQ_RENDERS / f"thumb-{sid}-final.jpg",
        SLUMBIQ_RENDERS / f"thumb-{sid}-final.png",
        SLUMBIQ_RENDERS / f"thumb-{sid}-final-v2.jpg",
        SLUMBIQ_RENDERS / f"thumb-{sid}-raw.png",
        SLUMBIQ_RENDERS / f"thumb-{sid}.png",
    ]
    for path in candidates:
        if path.exists():
            return str(path)
    return ""


def find_stills(video_id: str) -> list[str]:
    """Find available stills for a video. Falls back to thumbnail variants."""
    sid = video_id.lower().replace("-", "")
    stills_dir = SLUMBIQ_RENDERS / "stills"
    found: list[str] = []

    if stills_dir.exists():
        for pattern in [f"{sid}_*.png", f"{sid}_*.jpg"]:
            found.extend(str(p) for p in sorted(stills_dir.glob(pattern)))

    if found:
        return found[:3]

    fallbacks = [
        SLUMBIQ_RENDERS / f"thumb-{sid}-final.jpg",
        SLUMBIQ_RENDERS / f"thumb-{sid}-raw.png",
        SLUMBIQ_RENDERS / f"{sid}-visual-leo.jpg",
    ]
    return [str(p) for p in fallbacks if p.exists()][:3]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video-id", required=True, help="e.g. SL-001")
    parser.add_argument("--video-url", required=True, help="YouTube URL after upload")
    parser.add_argument("--video-title", required=True)
    parser.add_argument("--video-path", default="", help="Local mp4 path")
    parser.add_argument("--duration-hours", type=float, default=8.0)
    parser.add_argument("--theme", default="", help="e.g. rain_thunder_city")
    parser.add_argument("--script-summary", default="")
    parser.add_argument("--gumroad-url", default="")
    parser.add_argument("--gumroad-name", default="")
    parser.add_argument("--gumroad-price", type=float, default=0.0)
    args = parser.parse_args()

    MARKERS_DIR.mkdir(parents=True, exist_ok=True)

    gumroad_product = None
    if args.gumroad_url:
        gumroad_product = {
            "url": args.gumroad_url,
            "name": args.gumroad_name or "Slumbiq Pack",
            "price_usd": args.gumroad_price or 7,
        }

    marker = {
        "video_id": args.video_id,
        "video_title": args.video_title,
        "video_url": args.video_url,
        "video_path": args.video_path,
        "duration_hours": args.duration_hours,
        "theme": args.theme,
        "script_summary": args.script_summary,
        "thumbnail_path": find_thumbnail(args.video_id),
        "stills_paths": find_stills(args.video_id),
        "track_metadata": {"bpm": None, "frequency_hz": None, "binaural": False},
        "gumroad_product": gumroad_product,
        "marker_created_at": datetime.now(timezone.utc).isoformat(),
        "status": "pending",
    }

    marker_path = MARKERS_DIR / f"{args.video_id}.pending.json"
    with open(marker_path, "w") as f:
        json.dump(marker, f, indent=2)

    print(f"Marker written: {marker_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""
Slumbiq Blotato publisher.

Reads metadata.json from render_carousel.py output, pushes to Instagram, TikTok, and Twitter via Blotato.

Usage:
    python blotato_publish.py --metadata /Volumes/ClawDrive/renders/carousels/run_001/metadata.json --config brand_config.json

Set BLOTATO_API_KEY in environment before running.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import urllib.request
import urllib.error


def encode_image_b64(path: str) -> str:
    """Read image and return base64-encoded string."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def post_to_blotato(
    api_key: str,
    endpoint: str,
    payload: dict[str, Any],
    max_retries: int = 3,
) -> dict[str, Any]:
    """POST to Blotato with retries on transient failures."""
    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    last_error = None
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(endpoint, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            last_error = f"HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}"
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(last_error)
        except urllib.error.URLError as e:
            last_error = f"URL error: {e.reason}"
            time.sleep(2 ** attempt)
            continue

    raise RuntimeError(f"Blotato post failed after {max_retries} retries: {last_error}")


def build_caption(metadata: dict[str, Any], platform: str, brand: dict[str, Any]) -> str:
    """Build platform-specific caption."""
    base = metadata.get("caption", "")
    hashtags = metadata.get("hashtags", [])
    video_url = metadata.get("video_url", "")

    if platform == "instagram":
        tag_string = " ".join(f"#{tag}" for tag in hashtags)
        return f"{base}\n\n{tag_string}"

    if platform == "tiktok":
        tag_string = " ".join(f"#{tag}" for tag in hashtags[:5])
        return f"{base} {tag_string}"

    if platform == "twitter":
        short = base if len(base) <= 200 else base[:197] + "..."
        return f"{short}\n\n{video_url}"

    return base


def schedule_time(post_time_pref: str, timezone: str, hours_offset: int = 0) -> str:
    """Build ISO timestamp for scheduled post."""
    now = datetime.now(timezone.utc) + timedelta(hours=hours_offset)
    hour, minute = map(int, post_time_pref.split(":"))
    scheduled = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if scheduled < datetime.now(timezone.utc):
        scheduled += timedelta(days=1)
    return scheduled.isoformat()


def publish_instagram(
    metadata: dict[str, Any],
    config: dict[str, Any],
    api_key: str,
) -> dict[str, Any]:
    """Publish carousel to Instagram via Blotato."""
    images = [encode_image_b64(p) for p in metadata["rendered_files_ig"]]
    caption = build_caption(metadata, "instagram", config["brand"])
    payload = {
        "platform": "instagram",
        "account_handle": config["brand"]["instagram_handle"],
        "type": "carousel",
        "media": [{"data": img, "format": "png"} for img in images],
        "caption": caption,
        "schedule_at": schedule_time(
            config["blotato"]["post_time_preference"],
            config["blotato"]["timezone"],
        ),
    }
    return post_to_blotato(api_key, config["blotato"]["api_endpoint"], payload)


def publish_tiktok(
    metadata: dict[str, Any],
    config: dict[str, Any],
    api_key: str,
) -> dict[str, Any]:
    """Publish photo carousel to TikTok via Blotato."""
    images = [encode_image_b64(p) for p in metadata["rendered_files_tt"]]
    caption = build_caption(metadata, "tiktok", config["brand"])
    payload = {
        "platform": "tiktok",
        "account_handle": config["brand"]["tiktok_handle"],
        "type": "photo_carousel",
        "media": [{"data": img, "format": "png"} for img in images],
        "caption": caption,
        "schedule_at": schedule_time(
            config["blotato"]["post_time_preference"],
            config["blotato"]["timezone"],
            hours_offset=1,
        ),
    }
    return post_to_blotato(api_key, config["blotato"]["api_endpoint"], payload)


def publish_twitter(
    metadata: dict[str, Any],
    config: dict[str, Any],
    api_key: str,
) -> dict[str, Any]:
    """Publish first slide plus video link to Twitter via Blotato."""
    first_slide = metadata["rendered_files_ig"][0]
    image = encode_image_b64(first_slide)
    caption = build_caption(metadata, "twitter", config["brand"])
    payload = {
        "platform": "twitter",
        "account_handle": config["brand"]["twitter_handle"],
        "type": "single",
        "media": [{"data": image, "format": "png"}],
        "caption": caption,
        "schedule_at": schedule_time(
            config["blotato"]["post_time_preference"],
            config["blotato"]["timezone"],
            hours_offset=2,
        ),
    }
    return post_to_blotato(api_key, config["blotato"]["api_endpoint"], payload)


def append_log(log_path: str, entry: dict[str, Any]) -> None:
    """Append a JSON line to the pipeline log."""
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", required=True, help="metadata.json from render step")
    parser.add_argument("--config", required=True, help="Brand config JSON")
    parser.add_argument("--platforms", nargs="+", default=None, help="Override default platforms")
    parser.add_argument("--dry-run", action="store_true", help="Skip API calls, log only")
    args = parser.parse_args()

    with open(args.metadata, "r") as f:
        metadata = json.load(f)
    with open(args.config, "r") as f:
        config = json.load(f)

    api_key = os.environ.get(config["blotato"]["api_key_env"])
    if not api_key and not args.dry_run:
        print(f"Missing env var {config['blotato']['api_key_env']}", file=sys.stderr)
        return 1

    platforms = args.platforms or config["blotato"]["default_platforms"]
    publishers = {
        "instagram": publish_instagram,
        "tiktok": publish_tiktok,
        "twitter": publish_twitter,
    }

    results: dict[str, Any] = {}
    for platform in platforms:
        if platform not in publishers:
            results[platform] = {"status": "skipped", "reason": "unknown platform"}
            continue
        if args.dry_run:
            results[platform] = {"status": "dry_run", "would_post": True}
            continue
        try:
            response = publishers[platform](metadata, config, api_key)
            results[platform] = {"status": "scheduled", "response": response}
        except Exception as e:
            results[platform] = {"status": "failed", "error": str(e)}

    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "template": metadata.get("template"),
        "video_url": metadata.get("video_url"),
        "output_dir": metadata.get("output_dir"),
        "results": results,
    }
    append_log(config["paths"]["log_file"], log_entry)
    print(json.dumps(log_entry, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

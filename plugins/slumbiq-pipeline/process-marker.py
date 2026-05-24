"""
Process a single pending Slumbiq carousel marker through all three skills.

Called by Sevyn's main session after seeing SLUMBIQ_CAROUSEL_WORK_NEEDED.

Usage:
    python3 process-marker.py --marker ~/.openclaw/workspace/markers/carousel/SL-006.pending.json

Or batch:
    python3 process-marker.py --all

Flow per marker:
    1. Call Claude with the writer SKILL.md as system prompt + marker JSON as user message
    2. Save the resulting spec JSON next to the marker
    3. Run the renderer (subprocess) on the spec
    4. Run the scheduler (subprocess) on the rendered metadata
    5. Rename marker from .pending.json to .completed.json (or .failed.json)
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PLUGIN_ROOT = Path(__file__).parent.resolve()
MARKERS_DIR = Path.home() / ".openclaw" / "workspace" / "markers" / "carousel"
BRAND_CONFIG = Path("/Volumes/ClawDrive/scripts/slumbiq_pipeline/brand_config.json")
RENDERS_ROOT = Path("/Volumes/ClawDrive/renders/slumbiq/carousels")

WRITER_SKILL = PLUGIN_ROOT / "skills" / "slumbiq-carousel-writer" / "SKILL.md"
WRITER_EXAMPLES = PLUGIN_ROOT / "skills" / "slumbiq-carousel-writer" / "references" / "template-examples.md"
RENDERER_SCRIPT = PLUGIN_ROOT / "skills" / "slumbiq-carousel-renderer" / "render.py"
SCHEDULER_SCRIPT = PLUGIN_ROOT / "skills" / "slumbiq-carousel-scheduler" / "publish.py"

ANTHROPIC_ENDPOINT = "https://api.anthropic.com/v1/messages"
ANTHROPIC_MODEL = "claude-sonnet-4-5-20250929"


def call_writer(marker: dict[str, Any], api_key: str) -> dict[str, Any]:
    """Run the writer skill via the Anthropic API to produce a spec JSON."""
    with open(WRITER_SKILL, "r") as f:
        skill_md = f.read()
    with open(WRITER_EXAMPLES, "r") as f:
        examples_md = f.read()

    system_prompt = f"{skill_md}\n\n# template-examples.md (reference)\n\n{examples_md}"

    payload = {
        "model": ANTHROPIC_MODEL,
        "max_tokens": 2000,
        "system": system_prompt,
        "messages": [{"role": "user", "content": json.dumps(marker)}],
    }

    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    }

    req = urllib.request.Request(
        ANTHROPIC_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as response:
        body = json.loads(response.read().decode("utf-8"))

    text = "".join(block["text"] for block in body["content"] if block["type"] == "text").strip()
    if text.startswith("```"):
        text = "\n".join(line for line in text.split("\n") if not line.startswith("```"))

    return json.loads(text)


def process_marker(marker_path: Path, api_key: str, dry_run: bool = False) -> bool:
    """Process one pending marker. Returns True on success."""
    with open(marker_path, "r") as f:
        marker = json.load(f)

    video_id = marker["video_id"]
    print(f"[{video_id}] Processing marker...")

    try:
        print(f"[{video_id}] Calling writer...")
        spec = call_writer(marker, api_key)

        output_dir = RENDERS_ROOT / video_id
        output_dir.mkdir(parents=True, exist_ok=True)
        spec_path = output_dir / "carousel_spec.json"
        with open(spec_path, "w") as f:
            json.dump(spec, f, indent=2)

        print(f"[{video_id}] Rendering slides to {output_dir}...")
        result = subprocess.run(
            [
                sys.executable,
                str(RENDERER_SCRIPT),
                "--json", str(spec_path),
                "--config", str(BRAND_CONFIG),
                "--out", str(output_dir),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"Renderer failed: {result.stderr}")

        metadata_path = output_dir / "metadata.json"

        print(f"[{video_id}] Publishing via scheduler...")
        publish_cmd = [
            sys.executable,
            str(SCHEDULER_SCRIPT),
            "--metadata", str(metadata_path),
            "--config", str(BRAND_CONFIG),
        ]
        if dry_run:
            publish_cmd.append("--dry-run")
        publish_result = subprocess.run(publish_cmd)
        if publish_result.returncode != 0:
            raise RuntimeError("Scheduler returned non-zero")

        completed_path = marker_path.with_suffix("").with_suffix(".completed.json")
        marker["completed_at"] = datetime.now(timezone.utc).isoformat()
        marker["status"] = "completed"
        marker["run_dir"] = str(output_dir)
        with open(completed_path, "w") as f:
            json.dump(marker, f, indent=2)
        marker_path.unlink()

        print(f"[{video_id}] Done. {completed_path}")
        return True

    except Exception as e:
        failed_path = marker_path.with_suffix("").with_suffix(".failed.json")
        marker["failed_at"] = datetime.now(timezone.utc).isoformat()
        marker["status"] = "failed"
        marker["error"] = str(e)
        with open(failed_path, "w") as f:
            json.dump(marker, f, indent=2)
        marker_path.unlink()
        print(f"[{video_id}] FAILED: {e}", file=sys.stderr)
        return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--marker", help="Path to a specific pending marker")
    parser.add_argument("--all", action="store_true", help="Process every pending marker")
    parser.add_argument("--dry-run", action="store_true", help="Skip Blotato API calls")
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Missing ANTHROPIC_API_KEY", file=sys.stderr)
        return 1

    if args.all:
        markers = sorted(MARKERS_DIR.glob("*.pending.json"))
        if not markers:
            print("No pending markers")
            return 0
        success = 0
        for m in markers:
            if process_marker(m, api_key, args.dry_run):
                success += 1
        print(f"Processed {success}/{len(markers)} markers")
        return 0 if success == len(markers) else 1

    if args.marker:
        marker_path = Path(args.marker)
        if not marker_path.exists():
            print(f"Marker not found: {marker_path}", file=sys.stderr)
            return 1
        return 0 if process_marker(marker_path, api_key, args.dry_run) else 1

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())

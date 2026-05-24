# slumbiq-pipeline

End-to-end content pipeline for Slumbiq (@slumbiq), the ambient sleep YouTube channel.

## What this is

Sevyn plugin that turns every uploaded Slumbiq video into a branded carousel published across Instagram, TikTok, and Twitter. Runs autonomously after each YouTube upload completes.

## Skills

### slumbiq-carousel-writer (v0.1.0)
Reads a video's metadata (title, theme, script summary, thumbnail, stills, optional Gumroad product) and outputs a carousel spec JSON. Picks one of five templates (scene_breakdown, sleep_tip, track_of_night, bedtime_routine, gumroad_spotlight) based on the input. Writes on-brand headlines and sublines using the Slumbiq voice (dark, cinematic, cozy, no exclamation points, no hype).

### slumbiq-carousel-renderer (v0.1.0)
Takes a carousel spec and renders 1080x1350 Instagram portrait slides plus 1080x1920 TikTok vertical slides. Applies brand palette (deep black, cream serif headlines, amber sublines), vignetted thumbnails as backgrounds, and the SLEEP · FOCUS · CALM tagline anchor. Falls back to solid black if thumbnail files are missing.

### slumbiq-carousel-scheduler (v0.1.0)
Pushes rendered slides to Blotato. Selects hashtags per template, formats captions for each platform (full hashtag set for Instagram, top 5 for TikTok, short with link for Twitter), and schedules posts at staggered times in Asia/Bangkok timezone.

## Trigger architecture

Matches existing Sevyn queue-watcher pattern:

1. `slumbiq_upload_sl00X.py` finishes uploading a video to YouTube
2. `hooks/post-upload-marker.py` writes a marker file under `~/.openclaw/workspace/markers/carousel/`
3. `scripts/slumbiq-carousel-check.sh` runs periodically, scans for unprocessed markers
4. If markers exist, outputs `SLUMBIQ_CAROUSEL_WORK_NEEDED: N markers pending` to trigger main Claude session
5. Claude session runs the three skills in order, then deletes the marker

## Setup

```bash
claude plugin install slumbiq-pipeline@sevyn-skills
```

Then add this to your crontab or Launch Daemon (matches the heartbeat pattern of `slumbiq-pipeline-check.sh`):

```
*/5 * * * * /Users/moen/.claude/plugins/marketplaces/sevyn-skills/plugins/slumbiq-pipeline/scripts/slumbiq-carousel-check.sh
```

Add the post-upload hook call to the end of every `slumbiq_upload_sl00X.py`:

```python
# At the end of upload script, after upload completes:
import subprocess
subprocess.run([
    "python3",
    "/Users/moen/.claude/plugins/marketplaces/sevyn-skills/plugins/slumbiq-pipeline/hooks/post-upload-marker.py",
    "--video-id", "SL-001",
    "--video-url", uploaded_video_url,
    "--video-path", VIDEO_PATH,
])
```

## Environment variables

- `ANTHROPIC_API_KEY` for the writer skill (Claude Sonnet)
- `BLOTATO_API_KEY` for the scheduler skill

## Logs

All pipeline runs append to `/Volumes/ClawDrive/logs/carousel_pipeline.jsonl`.

## Future skills (planned)

- `slumbiq-audio-producer` - ambient track generation and mastering
- `slumbiq-youtube-uploader` - generalized version of the per-video upload scripts
- `slumbiq-gumroad-syncer` - automatic product creation when new track packs are ready

# slumbiq-carousel-scheduler

Publishes rendered Slumbiq carousels to Instagram, TikTok, and Twitter via Blotato. Runs last in the carousel chain.

## When to use

After slumbiq-carousel-renderer writes `metadata.json` into the run output directory. Reads the metadata, picks the final hashtag set, formats per-platform captions, and schedules the posts.

## Hashtag selection

The writer hands off a `hashtags_pool` (8-10 candidates). This scheduler picks the final set based on platform limits and template type. See `references/platform-formats.md` for the per-platform limits and selection logic.

Always include 3 core Slumbiq hashtags in every post: `sleepsounds`, `ambient`, `deepsleep`. Fill remaining slots from the pool.

## Platform formatting

### Instagram
- Full hashtag set (up to 10) appended to caption, separated by two newlines
- Image carousel format
- Scheduled at 20:00 Asia/Bangkok

### TikTok
- Top 5 hashtags inlined with caption
- Photo carousel format (TikTok now supports image carousels)
- Scheduled at 21:00 Asia/Bangkok (1 hour after Instagram to avoid duplicate notifications)

### Twitter
- First slide only, no carousel (Twitter limits)
- Caption truncated to 200 chars, then YouTube link appended
- No hashtags inline (Twitter culture)
- Scheduled at 22:00 Asia/Bangkok

## How it runs

Standalone Python script bundled in this skill directory:

```bash
python3 /Users/moen/.claude/plugins/marketplaces/sevyn-skills/plugins/slumbiq-pipeline/skills/slumbiq-carousel-scheduler/publish.py \
    --metadata /Volumes/ClawDrive/renders/slumbiq/carousels/SL-006/metadata.json \
    --config /Volumes/ClawDrive/scripts/slumbiq_pipeline/brand_config.json
```

Pass `--dry-run` during testing to skip actual API calls.

## Authentication

Requires `BLOTATO_API_KEY` environment variable. Set in `~/.zshrc` or the Launch Daemon plist.

## Logging

Appends one JSON line per run to `/Volumes/ClawDrive/logs/carousel_pipeline.jsonl` with timestamp, template, video URL, output dir, and per-platform status. While traveling, tail this file to monitor the pipeline.

## Failure handling

If one platform fails, the others still publish. Retry just the failed platform with `--platforms instagram` (or whichever failed). Each post's status lands in the log entry's `results` field.

## References

See `references/platform-formats.md` for hashtag selection logic per template, the exact JSON payload Blotato expects per platform, and the staggered scheduling rationale.

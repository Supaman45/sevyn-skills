# Platform Formats

How the scheduler picks hashtags, formats captions, and schedules posts per platform.

## Hashtag selection logic

The writer's `hashtags_pool` contains 7-10 candidates picked for the template. The scheduler narrows them down:

**Instagram**: take up to 10 hashtags from pool. Always include the 3 Slumbiq core tags (`sleepsounds`, `ambient`, `deepsleep`). Fill remaining 7 slots from the pool, in order. Append to caption with `\n\n` separator and `#` prefix on each.

**TikTok**: take top 5 hashtags from pool. Always include `sleepsounds` and `ambient`. Inline with caption, space-separated, with `#` prefix.

**Twitter**: no hashtags. Truncate caption to 200 chars (cut at last word boundary), append YouTube video URL on a new line.

## Per-template hashtag biases

Different templates need different secondary tags. The writer puts these in the pool, but the scheduler maintains this awareness as a sanity check:

- `scene_breakdown`: heavy on imagery tags (rainsounds, thunderstorm, fireplace, cozyvibes)
- `sleep_tip`: heavy on educational tags (sleephacks, sleepscience, betterSleep)
- `track_of_night`: heavy on music tags (sleepplaylist, ambientmusic, soundbath, focusmusic)
- `bedtime_routine`: heavy on wellness tags (bedtimeroutine, selfcare, wellness, nightroutine)
- `gumroad_spotlight`: heavy on commerce tags (digitalproducts, sleepaid, soundpack)

## Blotato payload format

### Instagram carousel

```json
{
  "platform": "instagram",
  "account_handle": "@slumbiq",
  "type": "carousel",
  "media": [
    {"data": "<base64 png>", "format": "png"},
    {"data": "<base64 png>", "format": "png"}
  ],
  "caption": "rain and thunder over a sleeping city. 8 hours, uninterrupted. link in bio.\n\n#sleepsounds #ambient #deepsleep #rainsounds #thunderstorm #asmr #sleepmusic #rainonroof #cozyvibes #nightroutine",
  "schedule_at": "2026-05-25T20:00:00+07:00"
}
```

### TikTok photo carousel

```json
{
  "platform": "tiktok",
  "account_handle": "@slumbiq",
  "type": "photo_carousel",
  "media": [{"data": "<base64 png>", "format": "png"}],
  "caption": "rain and thunder over a sleeping city. 8 hours, uninterrupted. link in bio. #sleepsounds #ambient #deepsleep #rainsounds #thunderstorm",
  "schedule_at": "2026-05-25T21:00:00+07:00"
}
```

### Twitter single image

```json
{
  "platform": "twitter",
  "account_handle": "@slumbiq",
  "type": "single",
  "media": [{"data": "<base64 png>", "format": "png"}],
  "caption": "rain and thunder over a sleeping city. 8 hours, uninterrupted. link in bio.\n\nhttps://youtube.com/watch?v=ABC123",
  "schedule_at": "2026-05-25T22:00:00+07:00"
}
```

## Why 20:00, 21:00, 22:00 Bangkok

The brand operates from Thailand. 20:00 to 22:00 Bangkok is:

- 13:00 to 15:00 UTC
- 09:00 to 11:00 EST (US East morning, peak sleep-content browsing on phones during commute)
- 06:00 to 08:00 PST (US West early morning, peak before-work browse)
- 14:00 to 16:00 BST (UK afternoon)

This window catches the US morning rush and UK afternoon simultaneously. The 1-hour stagger between platforms avoids duplicate notifications to users following @slumbiq across multiple platforms.

## Retry semantics

Each platform call has 3 retries with exponential backoff (2s, 4s, 8s). Retries trigger on HTTP 429 (rate limit) and 5xx errors. 4xx errors fail fast since they indicate bad payload.

If a platform ultimately fails, the log entry records `{"status": "failed", "error": "..."}` for that platform. Other platforms in the same run still publish independently.

To retry just the failed platform later:

```bash
python3 publish.py --metadata <path> --config <path> --platforms instagram
```

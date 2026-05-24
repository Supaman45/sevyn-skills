# slumbiq-carousel-writer

Picks a carousel template for a Slumbiq video and writes the headline, subline, caption, and hashtag set in the Slumbiq voice.

## When to use

Whenever a Slumbiq video finishes uploading to YouTube and a marker file appears at `~/.openclaw/workspace/markers/carousel/`. The marker file contains video metadata. This skill runs first in the carousel chain, before slumbiq-carousel-renderer and slumbiq-carousel-scheduler.

## Voice

Dark, cinematic, cozy. Sleep, focus, calm. Quiet voice at 11pm, not a marketer at 11am. Short lines. Confident.

Avoid: exclamation points, emojis in slide text, hype words (discover, unlock, transform, journey, embrace, dive, explore, amazing, incredible).

## Input

A JSON marker file with this shape:

```json
{
  "video_id": "SL-006",
  "video_title": "LoFi Rain & Thunder 8 Hours Sleep & Study Sounds",
  "video_url": "https://youtube.com/watch?v=ABC123",
  "duration_hours": 8,
  "theme": "rain_thunder_city",
  "script_summary": "Eight hours of layered rain and distant thunder over a sleeping city.",
  "thumbnail_path": "/Volumes/ClawDrive/renders/slumbiq/thumb-sl006-final.jpg",
  "stills_paths": ["..."],
  "track_metadata": {"bpm": null, "frequency_hz": null, "binaural": false},
  "gumroad_product": null
}
```

## Template selection

Pick one template per run. Rotate across videos so the feed stays varied.

- If `gumroad_product` is not null, 30% chance pick `gumroad_spotlight`
- If `script_summary` mentions a sleep technique, breathing pattern, or science point, pick `sleep_tip`
- If the video is a long ambient track with no science angle, default to `track_of_night` or `scene_breakdown`
- Every 5th run pick `bedtime_routine` to mix the feed

See `references/template-examples.md` for full schemas of each template with worked examples.

## Output format

Strict JSON only, no markdown fences, no preamble. The renderer reads stdout directly and crashes on extra characters. Pass the JSON through to the next skill via `~/.openclaw/workspace/markers/carousel/<video_id>.spec.json`.

## Writing rules for slide copy

Headline: 1 to 4 words, lowercase in the JSON (renderer uppercases for display), no punctuation.

Subline: 4 to 10 words, lowercase, period at end allowed.

Caption (for the post body, not slide text): one or two short lines. May include the YouTube link as "link in bio" or the @slumbiq handle.

## Hashtag selection

Hand off hashtag generation to slumbiq-carousel-scheduler. Do not include hashtags in slide text. Only include the platform-agnostic hashtag list in the spec JSON for the scheduler to filter.

## References

See `references/template-examples.md` for the five template schemas with full worked examples for a rain video, a fireplace video, a sleep tip video, a Gumroad product launch, and a bedtime routine post.

# Template Examples

Five carousel templates with worked examples. The writer picks one per video based on the selection logic in the main SKILL.md.

## Template 1: scene_breakdown (5 slides)

Best for: atmospheric ambient videos with strong visual themes (rain, storms, fireplaces, forests).

```json
{
  "template": "scene_breakdown",
  "video_url": "https://youtube.com/watch?v=ABC123",
  "video_id": "SL-006",
  "slides": [
    {"index": 1, "type": "hook", "image": "thumbnail_path", "headline": "tonight", "subline": "8 hours of rain and thunder"},
    {"index": 2, "type": "still_caption", "image": "stills_paths[0]", "headline": "the setting", "subline": "a sleeping city under storm"},
    {"index": 3, "type": "still_caption", "image": "stills_paths[1]", "headline": "the sound", "subline": "soft rain layered over distant thunder"},
    {"index": 4, "type": "still_caption", "image": "stills_paths[2]", "headline": "the purpose", "subline": "sleep onset in under 12 minutes"},
    {"index": 5, "type": "cta", "image": "thumbnail_path", "headline": "full 8 hours on youtube", "subline": "@slumbiq"}
  ],
  "caption": "rain and thunder over a sleeping city. 8 hours, uninterrupted. link in bio.",
  "hashtags_pool": ["sleepsounds", "rainsounds", "thunderstorm", "ambient", "deepsleep", "asmr", "sleepmusic", "rainonroof"]
}
```

## Template 2: sleep_tip (3 slides)

Best for: videos where the script touches on sleep science, breathing patterns, or behavioral techniques.

```json
{
  "template": "sleep_tip",
  "slides": [
    {"index": 1, "type": "tip_hook", "image": "thumbnail_path", "headline": "the 4-7-8 method", "subline": "for falling asleep faster"},
    {"index": 2, "type": "tip_body", "image": "stills_paths[0]", "headline": "how it works", "subline": "inhale 4 seconds. hold 7. exhale 8. repeat 4 times."},
    {"index": 3, "type": "cta", "image": "thumbnail_path", "headline": "pair it with tonight's track", "subline": "@slumbiq on youtube"}
  ],
  "caption": "one breathing pattern, eight hours of rain. sleep before slide 4.",
  "hashtags_pool": ["sleephacks", "sleepscience", "ambient", "deepsleep", "sleepsounds", "insomniarelief", "betterSleep"]
}
```

## Template 3: track_of_night (4 slides)

Best for: long-form ambient tracks without a strong narrative angle. The default for most uploads.

```json
{
  "template": "track_of_night",
  "slides": [
    {"index": 1, "type": "hook", "image": "thumbnail_path", "headline": "track of the night", "subline": "rain and thunder, 8 hours"},
    {"index": 2, "type": "still_caption", "image": "stills_paths[0]", "headline": "the mood", "subline": "cinematic. dark. slow."},
    {"index": 3, "type": "still_caption", "image": "stills_paths[1]", "headline": "best for", "subline": "deep sleep, study, focus"},
    {"index": 4, "type": "cta", "image": "thumbnail_path", "headline": "listen now", "subline": "@slumbiq on youtube"}
  ],
  "caption": "tonight's track. 8 hours uninterrupted.",
  "hashtags_pool": ["sleepplaylist", "ambientmusic", "soundbath", "sleepsounds", "deepsleep", "focusmusic", "studymusic"]
}
```

## Template 4: bedtime_routine (6 slides)

Best for: feed variety. Rotate in every fifth carousel.

```json
{
  "template": "bedtime_routine",
  "slides": [
    {"index": 1, "type": "hook", "image": "thumbnail_path", "headline": "the slumbiq routine", "subline": "for nights you need to disappear"},
    {"index": 2, "type": "step", "image": "stills_paths[0]", "headline": "step 1", "subline": "lights off by 10pm"},
    {"index": 3, "type": "step", "image": "stills_paths[1]", "headline": "step 2", "subline": "phone in another room"},
    {"index": 4, "type": "step", "image": "stills_paths[2]", "headline": "step 3", "subline": "4-7-8 breathing, two cycles"},
    {"index": 5, "type": "step", "image": "thumbnail_path", "headline": "step 4", "subline": "press play. eyes closed."},
    {"index": 6, "type": "cta", "image": "thumbnail_path", "headline": "tonight's track", "subline": "@slumbiq"}
  ],
  "caption": "four steps. eight hours. zero interruptions.",
  "hashtags_pool": ["bedtimeroutine", "selfcare", "sleepsounds", "wellness", "calm", "nightroutine", "sleepwell"]
}
```

## Template 5: gumroad_spotlight (4 slides)

Best for: any video with a `gumroad_product` field in the input. Drives store traffic.

```json
{
  "template": "gumroad_spotlight",
  "slides": [
    {"index": 1, "type": "product_hook", "image": "thumbnail_path", "headline": "rain pack vol 1", "subline": "10 tracks. studio quality. yours forever."},
    {"index": 2, "type": "still_caption", "image": "stills_paths[0]", "headline": "what's inside", "subline": "rain, thunder, fireplace, wind, storm loops"},
    {"index": 3, "type": "still_caption", "image": "stills_paths[1]", "headline": "made for", "subline": "creators, sleepers, deep workers"},
    {"index": 4, "type": "cta", "image": "thumbnail_path", "headline": "slumbiq.gumroad.com", "subline": "$7. one time. no subscription."}
  ],
  "caption": "ten ambient tracks. studio quality. seven dollars.",
  "hashtags_pool": ["digitalproducts", "sleepaid", "ambient", "deepsleep", "focusmusic", "soundpack", "creators"]
}
```

## Worked example: a fireplace video

Input:
```json
{
  "video_id": "SL-007",
  "video_title": "Cozy Fireplace + Rain + Wind 8 Hours Sleep Sounds",
  "theme": "fireplace_rain_wind",
  "script_summary": "Eight hours of crackling fireplace layered with steady rain and gentle wind. Designed for cold nights and deep recovery sleep.",
  "gumroad_product": null
}
```

Choose: `scene_breakdown` (atmospheric, no science angle, no product). Output:

```json
{
  "template": "scene_breakdown",
  "video_url": "https://youtube.com/watch?v=XYZ789",
  "video_id": "SL-007",
  "slides": [
    {"index": 1, "type": "hook", "image": "thumbnail_path", "headline": "tonight", "subline": "fireplace, rain, wind. 8 hours."},
    {"index": 2, "type": "still_caption", "image": "stills_paths[0]", "headline": "the setting", "subline": "a cabin in a storm"},
    {"index": 3, "type": "still_caption", "image": "stills_paths[1]", "headline": "the sound", "subline": "crackling wood under steady rain"},
    {"index": 4, "type": "still_caption", "image": "stills_paths[2]", "headline": "the purpose", "subline": "warmth on cold nights"},
    {"index": 5, "type": "cta", "image": "thumbnail_path", "headline": "full 8 hours on youtube", "subline": "@slumbiq"}
  ],
  "caption": "fireplace, rain, wind. cabin in a storm. 8 hours. link in bio.",
  "hashtags_pool": ["sleepsounds", "fireplace", "rainsounds", "cozyvibes", "ambient", "deepsleep", "asmr", "winternight"]
}
```

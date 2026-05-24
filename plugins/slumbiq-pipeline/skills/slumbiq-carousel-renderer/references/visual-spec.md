# Visual Spec

Concrete numbers behind the Slumbiq carousel renderer.

## Colors

```
background:        #0A0A0F
background_overlay: #000000B3 (70% black for vignette)
primary_text:      #F5E6D3  (cream, used for headlines)
accent_amber:      #D4A574  (warm amber, used for sublines)
accent_warm:       #E8B87A  (brighter amber, used for CTA handle)
muted_text:        #9A8B7A  (used for SLEEP · FOCUS · CALM tagline)
divider:           #2A2520  (rarely used)
```

These were extracted from the Slumbiq YouTube banner (the candle and rain banner).

## Dimensions

- Instagram portrait carousel: 1080 x 1350
- TikTok vertical carousel: 1080 x 1920
- Square (reserved for future): 1080 x 1080
- Twitter image (reserved for future): 1200 x 675

## Font sizes (relative to canvas height)

- Headline: `int(h * 0.085)` (≈ 115px at IG height, 163px at TikTok height)
- Subline: `int(h * 0.032)` (≈ 43px IG, 61px TikTok)
- Accent (handle, tagline): `int(h * 0.022)` (≈ 30px IG, 42px TikTok)

## Text positioning

- Hook, CTA, product_hook slides: text centered vertically in middle of canvas
- Still caption, tip body, step slides: text positioned in lower third (start_y = h * 0.62)
- SLEEP · FOCUS · CALM anchor: always at y = h * 0.93
- @slumbiq handle (CTA only): at y = h * 0.05

## Vignette

The renderer applies a radial darkening from edges toward center on any slide that has a background image. Implementation:

- 20 concentric rectangles drawn on a mask layer
- Padding scales as `(min(w, h) / 2 - 1) / 20` per step
- Alpha decreases from `255 * strength` to 0
- Gaussian blur with radius `min(w, h) / 9`
- Composite the image over solid black using the mask

This guards against the earlier bug where fixed pixel padding (30px * 20 = 600px) would invert rectangles on small images.

## Background image processing

- Resize to cover target dimensions (center-cropped if aspect ratios differ)
- Brightness reduced to 45% via PIL ImageEnhance
- Then vignette applied

This darkens the image enough to read cream text on top while preserving the moody atmosphere of Slumbiq thumbnails.

## Text wrapping

Headlines and sublines auto-wrap to fit `max_text_width = w - (2 * margin_x)` where `margin_x = w * 0.08`. Line height for headlines is `headline_size * 1.1`. Line height for sublines is `subline_size * 1.4`.

## Why Georgia and Helvetica fallbacks work

When Cormorant Garamond Bold isn't available, PIL falls back to Georgia. Georgia is a transitional serif designed for screen reading. It carries similar editorial weight to Cormorant and renders cleanly at all sizes. The cream-on-black combination plus the warm amber subline reads as intentional even with the fallback.

When Inter isn't available, Helvetica steps in. The neutral grotesque works fine since the subline is a supporting role, not a hero.

The brand will look 5-10% sharper with Cormorant + Inter installed, but the fallback is professional, not amateur.

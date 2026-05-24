# slumbiq-carousel-renderer

Renders a carousel spec into branded PNG slides. Runs after slumbiq-carousel-writer.

## When to use

After a `<video_id>.spec.json` file appears in `~/.openclaw/workspace/markers/carousel/`. Reads the spec, produces Instagram 1080x1350 and TikTok 1080x1920 slide pairs, writes metadata.json for the scheduler.

## Brand visual

- Background: deep black `#0A0A0F`
- Primary text: cream `#F5E6D3` (Georgia serif fallback works well)
- Accent: warm amber `#D4A574`
- Muted text: `#9A8B7A`
- Tagline: SLEEP · FOCUS · CALM anchored at bottom
- Vignette darkening on thumbnail backgrounds to make text pop

## How it runs

Standalone Python script bundled in this skill directory. Sevyn invokes it via subprocess:

```bash
python3 /Users/moen/.claude/plugins/marketplaces/sevyn-skills/plugins/slumbiq-pipeline/skills/slumbiq-carousel-renderer/render.py \
    --spec ~/.openclaw/workspace/markers/carousel/SL-006.spec.json \
    --config /Volumes/ClawDrive/scripts/slumbiq_pipeline/brand_config.json \
    --out /Volumes/ClawDrive/renders/slumbiq/carousels/SL-006
```

## Dependencies

- Python 3.10+
- Pillow (install via `pip install Pillow` in the venv at `/Volumes/ClawDrive/scripts/slumbiq_pipeline/venv`)

## Fallback behavior

If thumbnail or stills paths in the spec don't exist on disk, the renderer uses a solid dark background and proceeds. Output is still publishable, just without the atmospheric imagery underneath.

If brand fonts (Cormorant, Inter) aren't installed, falls back to Georgia and Helvetica. Tested output looks clean.

## Output

For a spec with N slides, produces:

- `slide_1.png` through `slide_N.png` (Instagram portrait)
- `slide_1_tt.png` through `slide_N_tt.png` (TikTok vertical)
- `metadata.json` containing caption, hashtags_pool, video_url, and file paths for the scheduler

## References

See `references/visual-spec.md` for color codes, font sizes per dimension, vignette strength, text positioning logic, and the exact PIL operations used.

"""
Slumbiq carousel renderer.

Reads carousel JSON from the agent, produces branded PNG slides.

Usage:
    python render_carousel.py --json carousel_spec.json --config brand_config.json --out /Volumes/ClawDrive/renders/carousels/run_001

The output directory will contain:
    slide_1.png ... slide_N.png  (1080x1350 Instagram portrait)
    slide_1_tt.png ... slide_N_tt.png  (1080x1920 TikTok)
    metadata.json  (caption, hashtags, source video url)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


def load_font(path: str, size: int, fallback: str) -> ImageFont.FreeTypeFont:
    """Load a font with graceful fallback to system fonts."""
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        try:
            return ImageFont.truetype(fallback, size)
        except (OSError, IOError):
            return ImageFont.load_default()


def darken_image(img: Image.Image, factor: float = 0.55) -> Image.Image:
    """Darken background image so text reads cleanly."""
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(factor)


def fit_cover(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    """Resize image to cover target dimensions, center-cropped."""
    src_w, src_h = img.size
    scale = max(target_w / src_w, target_h / src_h)
    new_w, new_h = int(src_w * scale), int(src_h * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return img.crop((left, top, left + target_w, top + target_h))


def apply_vignette(img: Image.Image, strength: float = 0.7) -> Image.Image:
    """Add radial darkening from edges to focus center."""
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    steps = 20
    max_pad = min(w, h) // 2 - 1
    pad_step = max_pad / steps
    for i in range(steps):
        alpha = int(255 * (1 - i / steps) * strength)
        pad = int(i * pad_step)
        x0, y0 = pad, pad
        x1, y1 = w - pad, h - pad
        if x1 <= x0 or y1 <= y0:
            break
        draw.rectangle([x0, y0, x1, y1], fill=alpha)
    blur_radius = min(w, h) // 9
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))
    black = Image.new("RGB", (w, h), (0, 0, 0))
    return Image.composite(img, black, mask)


def draw_text_centered(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    canvas_w: int,
    y: int,
    color: str,
) -> int:
    """Draw text horizontally centered. Returns the height drawn."""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (canvas_w - text_w) // 2
    draw.text((x, y), text, fill=color, font=font)
    return text_h


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.ImageDraw) -> list[str]:
    """Wrap text into lines that fit max_width."""
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        test = " ".join(current + [word])
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def render_slide(
    slide: dict[str, Any],
    config: dict[str, Any],
    dimensions: tuple[int, int],
    output_path: Path,
) -> None:
    """Render one slide to a PNG file."""
    w, h = dimensions
    colors = config["colors"]
    fonts = config["fonts"]

    image_path = slide.get("image")
    if image_path and os.path.exists(image_path):
        bg = Image.open(image_path).convert("RGB")
        bg = fit_cover(bg, w, h)
        bg = darken_image(bg, 0.45)
        bg = apply_vignette(bg, 0.55)
    else:
        bg = Image.new("RGB", (w, h), colors["background"])

    draw = ImageDraw.Draw(bg)

    headline_size = int(h * 0.085)
    subline_size = int(h * 0.032)
    accent_size = int(h * 0.022)

    headline_font = load_font(fonts["heading_path"], headline_size, fonts["heading_fallback"])
    subline_font = load_font(fonts["body_path"], subline_size, fonts["body_fallback"])
    accent_font = load_font(fonts["accent_path"], accent_size, fonts["body_fallback"])

    headline = slide.get("headline", "").upper()
    subline = slide.get("subline", "")
    slide_type = slide.get("type", "")

    margin_x = int(w * 0.08)
    max_text_width = w - (2 * margin_x)

    headline_lines = wrap_text(headline, headline_font, max_text_width, draw)
    subline_lines = wrap_text(subline, subline_font, max_text_width, draw)

    line_height_h = int(headline_size * 1.1)
    line_height_s = int(subline_size * 1.4)
    headline_block = line_height_h * len(headline_lines)
    subline_block = line_height_s * len(subline_lines)
    gap = int(h * 0.04)
    total_block = headline_block + gap + subline_block

    start_y = int(h * 0.62)
    if slide_type in ("hook", "cta", "product_hook"):
        start_y = int((h - total_block) / 2)

    y = start_y
    for line in headline_lines:
        draw_text_centered(draw, line, headline_font, w, y, colors["primary_text"])
        y += line_height_h

    y += gap

    for line in subline_lines:
        draw_text_centered(draw, line, subline_font, w, y, colors["accent_amber"])
        y += line_height_s

    brand_label = config["brand"]["tagline"]
    brand_y = int(h * 0.93)
    draw_text_centered(draw, brand_label, accent_font, w, brand_y, colors["muted_text"])

    if slide_type == "cta":
        handle = config["brand"]["handle"]
        handle_y = int(h * 0.05)
        draw_text_centered(draw, handle, accent_font, w, handle_y, colors["accent_amber"])

    bg.save(output_path, "PNG", quality=95)


def render_all(spec_path: str, config_path: str, output_dir: str) -> dict[str, Any]:
    """Render all slides from a carousel spec."""
    with open(spec_path, "r") as f:
        spec = json.load(f)
    with open(config_path, "r") as f:
        config = json.load(f)

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    ig_dims = tuple(config["dimensions"]["instagram_carousel"])
    tt_dims = tuple(config["dimensions"]["tiktok_carousel"])

    rendered_files: list[str] = []
    for slide in spec["slides"]:
        idx = slide["index"]
        ig_path = out / f"slide_{idx}.png"
        tt_path = out / f"slide_{idx}_tt.png"
        render_slide(slide, config, ig_dims, ig_path)
        render_slide(slide, config, tt_dims, tt_path)
        rendered_files.append(str(ig_path))

    metadata = {
        "template": spec.get("template"),
        "video_url": spec.get("video_url"),
        "caption": spec.get("caption"),
        "hashtags": spec.get("hashtags"),
        "rendered_files_ig": [str(out / f"slide_{s['index']}.png") for s in spec["slides"]],
        "rendered_files_tt": [str(out / f"slide_{s['index']}_tt.png") for s in spec["slides"]],
        "output_dir": str(out),
    }

    with open(out / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    return metadata


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", required=True, help="Carousel spec JSON path")
    parser.add_argument("--config", required=True, help="Brand config JSON path")
    parser.add_argument("--out", required=True, help="Output directory")
    args = parser.parse_args()

    try:
        metadata = render_all(args.json, args.config, args.out)
        print(json.dumps(metadata, indent=2))
        return 0
    except Exception as e:
        print(f"Render failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

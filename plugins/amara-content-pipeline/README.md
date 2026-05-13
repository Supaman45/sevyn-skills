# amara-content-pipeline

End-to-end content pipeline for Amara (@amara.stx), the Quiet Biohacker AI influencer.

## What this plugin does

Bundles three skills that together handle the full content creation flow for Amara:

1. **Generate the visual** — `amara-prompt-builder` constructs Higgsfield Soul 2.0 prompts with Soul ID locked, pillar-aware, in the amateur phone aesthetic.

2. **Write the caption** — `amara-voice-writer` produces three caption options in Amara's Quiet Biohacker voice, each using a different structural template.

3. **Schedule the post** — `amara-content-scheduler` pushes the chosen image and caption through Blotato MCP to IG, TikTok, and Twitter with platform-specific formatting and the right hashtag block.

## How the skills work together

```
User request
    ↓
amara-prompt-builder  →  Higgsfield Soul 2.0 generates images
    ↓
amara-voice-writer    →  Drafts 3 caption options
    ↓
amara-content-scheduler  →  Blotato schedules across platforms
```

In autonomous mode (via Sevyn AI + Telegram approval), the user receives images and captions in Telegram, replies with a selection code, and the scheduler executes.

## Required infrastructure

- Higgsfield MCP connected, Amara's Soul ID trained and accessible
- Blotato MCP connected, all three Amara accounts authenticated
- Anthropic API access (for caption generation)
- Optional: n8n workflow for autonomous scheduling
- Optional: Telegram bot (@amara_stx_bot) for approval flow

## Voice and aesthetic anchors

Amara's positioning: The Quiet Biohacker. Recovery-first, data-precise, feminine-coded biohacking. College-girl-cute aesthetic with subtle everyday makeup, linen and cream palette, amateur phone-shot capture quality.

See individual SKILL.md files for full voice rules, banned words, pillar definitions, and prompt templates.

## Version

0.1.0 — initial release, manual approval flow.

## Roadmap

- v0.2.0: Carousel batch support (5-slide generation with single caption)
- v0.3.0: Reel automation (Soul 2.0 → Kling I2V → scheduled reel)
- v0.4.0: Auto-engagement (Sevyn replies to comments in Amara's voice)
- v0.5.0: Performance scoring (caption A/B testing against engagement data)

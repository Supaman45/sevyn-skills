# sevyn-skills

Private Claude Code skill marketplace for Sevyn AI operations. Distributes skills across all brand pipelines (Amara, The Town Weekly, Brnstak, Slumbiq) with version control, auto-update, and rollback via git.

## What this is

A Claude Code plugin marketplace. Skills live as plugins in this repo, get distributed via `marketplace.json`, and auto-update on every Claude Code session launch once you enable auto-update.

## Setup

On any machine running Claude Code (Mac Mini, laptop, etc.):

```bash
claude plugin marketplace add seri/sevyn-skills
claude plugin install amara-content-pipeline@sevyn-skills
```

Then enable auto-update in the `/plugin` TUI so every session pulls the latest versions automatically.

## Current plugins

### amara-content-pipeline (v0.1.0)

End-to-end content pipeline for @amara.stx. Bundles three skills:

- `amara-voice-writer` — generates captions in Amara's Quiet Biohacker voice
- `amara-prompt-builder` — constructs Higgsfield Soul 2.0 prompts with Soul ID locked
- `amara-content-scheduler` — schedules posts via Blotato MCP across IG, TikTok, Twitter

## Planned plugins

- `town-weekly-pipeline` — Tacoma news scoring, summarization, Beehiiv formatting
- `brnstak-research` — YouTube research, voiceover script generation, Blotato scheduling
- `slumbiq-pipeline` — ambient audio production, YouTube upload automation, Gumroad sync

## Repo structure

```
sevyn-skills/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   └── amara-content-pipeline/
│       ├── .claude-plugin/plugin.json
│       └── skills/
│           ├── amara-voice-writer/
│           ├── amara-prompt-builder/
│           └── amara-content-scheduler/
└── README.md
```

## Versioning

Semantic versioning per plugin. Update the version in `plugin.json` and `marketplace.json` whenever a skill is modified. Tag git releases for major versions.

## Self-iteration roadmap

Phase 3 of the Sevyn AI build wires this repo into the skill-evolution-loop. Sevyn runs nightly experiments on skill files, scores outputs against a test set, commits accepted improvements, and pushes to this repo. Every Claude session picks up improvements automatically on next launch.

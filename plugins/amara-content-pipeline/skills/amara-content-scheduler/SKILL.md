---
name: amara-content-scheduler
description: Schedule Amara's social posts through Blotato MCP across Instagram, TikTok, and Twitter. Use whenever the user wants to post, publish, schedule, queue, or send any Amara content to her social accounts. Owns the per-pillar hashtag blocks and per-pillar optimal posting times.
---

# Amara Content Scheduler

Pushes Amara content through Blotato MCP. Owns hashtag selection, posting times, AI-content compliance flags. Source of truth for the per-pillar hashtag blocks.

## Required pre-flight checks

Before scheduling any post, confirm:

1. Caption is locked (came from amara-voice-writer or user-provided).
2. Image or video is hosted at a public URL (Higgsfield CloudFront, S3, or uploaded via `blotato_create_presigned_upload_url`).
3. Target platforms are specified by the user.
4. Schedule time is specified.
5. Content pillar is identified so the right hashtag block applies.

If any of these are missing, ask the user. Do not guess defaults.

## Amara's connected accounts

- Instagram: @amara.stx
- TikTok: @amara.stx
- Twitter: @AmaraStx

All three are connected via Blotato MCP. Use `blotato_list_accounts` to confirm IDs if not in recent context.

## Content rotation

Default mix: **~80% lifestyle (Pillars 1-4), ~20% wellness (Pillar 5)**. A weekly cadence of 5-7 posts looks like 4-6 lifestyle + 1 wellness, where the wellness post is the affiliate-active vehicle.

This ratio is a starting point. Revisit after 2-3 weeks of posting based on engagement data:
- If biohacker overperforms or affiliate conversion is strong, push to 70/30.
- If lifestyle dominates engagement, hold or push to 85/15.

Tune based on data, not assumptions.

## Hashtag strategy

Hashtags are critical for IG reach. Captions never include hashtags inline; they're appended as a separate block at the end of the caption (handled by amara-voice-writer at caption-generation time).

**Target per IG post:** 15-20 hashtags. Mix three tiers:
- **Tier 1, large reach (1M+ posts)**: ~5 broad pillar tags for new-eye exposure.
- **Tier 2, mid reach (100k-1M)**: ~7-8 specific tags where her content competes well.
- **Tier 3, niche (<100k)**: ~5-7 community tags where she lands on top results and gets saved/shared.

Avoid known shadowbanned tags. Refresh the blocks quarterly.

## Hashtag blocks by pillar

This file is the canonical source. amara-voice-writer/SKILL.md inlines the same blocks so the n8n caption-gen runtime sees them via its fetched system prompt. Keep both files in sync when refreshing.

### Pillar 1, Night out

**IG block:**
#nightout #girlsnight #partyvibes #datenight #weekendvibes #outfitinspo #ootn #ootd #nycnights #rooftopvibes #downtowngirl #latedinner #cocktailbar #miniskirt #cityvibes #drinksout #saturdaynightout #goingoutoutfit #partyfit #afterhoursaesthetic

**TikTok block:** #fyp #nightout #grwm #goingoutoutfit #partyvibes

### Pillar 2, Cozy home

**IG block:**
#cozyaesthetic #homebody #sundayreset #selfcare #slowmornings #cozygirl #weekendmood #loungewear #candlelight #sundayfunday #bedrotting #softgirlaesthetic #cleangirl #sundayritual #pjsallday #cozynight #homevibes #stayinaesthetic #wintersundays #couchpotato

**TikTok block:** #fyp #cozyaesthetic #sundayreset #homebody #softgirlaesthetic

### Pillar 3, Getting ready

**IG block:**
#ootd #getreadywithme #grwm #fitcheck #outfitideas #outfitoftheday #styleinspo #mirrorselfie #fashioninspo #glamcore #stylediary #fitfinds #neutralstyle #capsulewardrobe #closetdiaries #everydaystyle #thatgirlaesthetic #outfitcheck #beforegoingout #fittotry

**TikTok block:** #fyp #grwm #fitcheck #ootd #styleinspo

### Pillar 4, Daytime out

**IG block:**
#coffee #citygirl #weekendmood #brunchspot #walkwithme #coffeegirlie #matchamoment #slowliving #citywalk #parkdays #morningroutine #cafehopping #walkingcity #latteart #saturdayerrands #cityaesthetic #cafelife #brunchtime #daytimevibes #coffeeshopvibes

**TikTok block:** #fyp #coffeegirlie #citywalk #slowliving #brunchspot

### Pillar 5, Wellness / biohacker (affiliate pillar)

**IG block:**
#biohacking #wellnessjourney #recovery #holistichealth #longevity #peptidetherapy #redlighttherapy #hrv #mitochondrialhealth #cyclesync #bpc157 #microdosing #sleepoptimization #parasympatheticactivation #cgmlife #femalebiohacker #recoveryprotocol #ouraring #whoopstrap #wellnessoptimization

**TikTok block:** #fyp #biohacking #wellnesstok #recovery #femalebiohacker

## Optimal posting times (IG)

Tune posting time to pillar — the audience's window matches the content:

- **Pillar 1 (Night out)**: Saturday night 9-11pm Pacific. Audience is also out; post lands in-context.
- **Pillar 2 (Cozy home)**: Sunday 6-8pm Pacific. Week wind-down window.
- **Pillar 3 (Getting ready)**: Friday or Saturday 5-7pm Pacific (pre-going-out scroll). Or any weekday 11am-1pm for daytime GRWM.
- **Pillar 4 (Daytime out)**: Tuesday-Thursday 11am-1pm Pacific. Lunch break and mid-day scroll peaks.
- **Pillar 5 (Wellness)**: Sunday 6-8pm Pacific (reset window) or Tuesday-Thursday 11am-1pm. Higher save/share intent both times.

General fallback: Tuesday-Thursday 11am-1pm Pacific is the safest catch-all.

For multi-platform same-day posts, stagger by 1-2 hours so the same caption doesn't hit every feed simultaneously.

## Platform-specific formatting

### Instagram
- Caption length: up to 2,200 chars; keep body under 600 for engagement.
- Hashtags: 15-20 mixed tiers, appended after caption with a blank line separator.
- Media: single image feed, up to 10 for carousel, 9:16 for reels.
- AI disclosure: handled in profile bio.

### TikTok
- Caption length: under 300 chars total including hashtags.
- Hashtags: 3-5 only. Mix #fyp with niche tags.
- Media: video only, 9:16, 9-60s.
- AI disclosure: always `isAiGenerated: true`.

### Twitter
- Caption length: under 240 chars.
- Hashtags: 0-2 max. Often zero is best.
- Media: single image or up to 4 in a thread.

## How the n8n pipeline uses these blocks

The Anthropic caption-gen node fetches `amara-voice-writer/SKILL.md` at runtime as its system prompt. That file inlines the same hashtag blocks listed here and instructs Claude to append the block matching the queue row's `pillar` value after the three caption options. Once the user picks A/B/C in Telegram, the chosen caption already has its hashtag block attached.

Keep this file and voice-writer in sync whenever you refresh blocks.

## The posting flow

When the user gives the go-ahead:

1. Confirm Blotato MCP is connected (`blotato_list_accounts` if no accounts in context).
2. If image is local, generate a presigned upload URL via `blotato_create_presigned_upload_url`, push bytes, get public URL.
3. If image is from Higgsfield, use its CloudFront URL directly.
4. The caption already includes its hashtag block (appended at caption-gen time).
5. Call `blotato_create_post` once per platform.
6. For TikTok, always set `isAiGenerated: true`.
7. Confirm scheduled time and post IDs back to the user.
8. Log the post to `amara_content_log`.

## Error handling

If a post fails:
1. Read the error from Blotato.
2. Common failures: media URL unreachable, account disconnected, character limit exceeded.
3. Report the specific failure with a fix suggestion. Never silently retry.

## Approval workflow integration

When triggered by Sevyn AI via Telegram approval:
1. Parse the selection code ("2B post 7am tuesday" → image 2, caption B, next Tuesday 7am Pacific).
2. Pull the image from the Higgsfield generation set.
3. Pull the chosen caption (already includes the hashtag block).
4. Confirm platform (default to last preference).
5. Execute posting flow.
6. Reply confirming queued.

## Content logging

After each successful post, append to `amara_content_log`:

| Date | Platform | Pillar | Caption preview | Image URL | Post URL | Scheduled time | Status |

## References

See `references/hashtags.json` for machine-readable hashtag sets.
See `references/posting-schedule.md` for cadence guidance.

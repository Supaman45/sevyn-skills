---
name: amara-content-scheduler
description: Schedule Amara's social posts through Blotato MCP across Instagram, TikTok, and Twitter. Use whenever the user wants to post, publish, schedule, queue, or send any Amara content to her social accounts. Always trigger when the user references posting, scheduling, going live, or pushing content for @amara.stx, regardless of phrasing.
---

# Amara Content Scheduler

Pushes Amara content through Blotato MCP with platform-specific formatting, hashtag selection, and AI-content compliance flags.

## Required pre-flight checks

Before scheduling any post, confirm:

1. Caption is locked (came from amara-voice-writer or user-provided).
2. Image or video is hosted at a public URL (Higgsfield CloudFront, S3, or has been uploaded via blotato_create_presigned_upload_url).
3. Target platforms are specified by the user (IG, TikTok, Twitter, or combination).
4. Schedule time is specified (post now, or specific date and hour with timezone).
5. Content pillar is identified so the right hashtag block applies.

If any of these are missing, ask the user. Do not guess defaults.

## Amara's connected accounts

- Instagram: @amara.stx
- TikTok: @amara.stx
- Twitter: @AmaraStx

All three accounts are connected via Blotato MCP. Use `blotato_list_accounts` to confirm IDs before posting if they are not in recent context.

## Platform-specific formatting rules

### Instagram

- Caption length: up to 2,200 characters but keep under 600 for engagement.
- Hashtags: 18 to 25 mixed big/mid/niche, placed after caption with a line break separator.
- Media: single image for feed post, up to 10 images for carousel, vertical 9:16 for reels.
- AI disclosure: include subtle disclosure in profile bio rather than per-post (existing setup).

### TikTok

- Caption length: under 300 characters total including hashtags.
- Hashtags: 3 to 5 only. Mix #fyp with niche tags. More than 5 hurts reach.
- Media: video only, vertical 9:16, 9 to 60 seconds.
- AI disclosure: always set `isAiGenerated: true` flag for Amara content (compliance requirement).

### Twitter

- Caption length: under 240 characters to leave engagement space.
- Hashtags: 0 to 2 maximum. Often best with zero.
- Media: single image or up to 4 in a thread.
- No special AI disclosure flag required.

## Hashtag blocks by pillar

Pull the right block based on content pillar identified by amara-prompt-builder or stated by the user.

### Pillar 1, Morning Protocol

IG block:
#morningroutine #biohacking #femalebiohacker #wellnessmorning #morningprotocol #ouraring #circadianhealth #cortisolawakening #wellnesscreator #recoveryfocused #cleangirlaesthetic #wellnessjourney #healthylifestyle #morningwellness #adaptogen #lightexposure #sleephygiene #wellnessroutine #biohackingfemale #hormonebalance

TikTok block: #fyp #morningroutine #biohacking #wellnesstok #femalebiohacker

### Pillar 2, Protocol Education

IG block:
#biohacking #femalebiohacker #womenshealth #hormonebalance #supplementprotocol #peptidetherapy #magnesiumglycinate #creatineforwomen #wellnesseducation #protocoldesign #wellnesscreator #cyclesyncing #lutealphase #follicularphase #womenshormones #researchbacked #wellnessresearch #healthoptimization #wellnessjourney #recoveryfocused

TikTok block: #fyp #biohacking #wellnesstok #womenshealth #educational

### Pillar 3, Recovery Rituals

IG block:
#recoveryday #parasympathetic #nervoussystemregulation #vagusnerve #saunatherapy #coldexposure #recoveryprotocol #wellnessritual #stressrelief #cortisolregulation #wellnesscreator #biohacking #femalebiohacker #breathwork #recoverytools #healthylifestyle #wellnessjourney #infraredsauna #redlighttherapy #podwalk

TikTok block: #fyp #recovery #saunatok #coldplunge #wellnesstok

### Pillar 4, Wearable Data and Training

IG block:
#ouraring #whoop #hrvtraining #zone2cardio #zone2training #pilatesathome #strengthforwomen #wearabledata #datadrivenfitness #recoveryfocused #cgmcontinuous #glucosetracking #biohacking #femalebiohacker #wellnesscreator #functionalfitness #womensfitness #wellnessjourney #healthtracking #wellnessdata

TikTok block: #fyp #ouraring #whoop #zone2 #wellnesstok

## Optimal posting times

Default to these unless user overrides:

- Instagram feed and carousel: 7am or 6pm Pacific (engagement peaks at start and end of day).
- Instagram reel: 11am or 7pm Pacific.
- TikTok: 7am, 12pm, or 9pm Pacific.
- Twitter: 8am or 5pm Pacific.

For multi-platform same-day posts, stagger by 1 to 2 hours so the same caption does not hit all feeds simultaneously.

## The posting flow

When the user gives the go-ahead, execute in this order:

1. Confirm Blotato MCP is connected (call `blotato_list_accounts` if no accounts in recent context).
2. If image is local, generate a presigned upload URL via `blotato_create_presigned_upload_url`, push the bytes, get the public URL.
3. If image is from Higgsfield, the CloudFront URL is already public, use it directly.
4. Append the right hashtag block to the caption based on pillar and platform.
5. Call `blotato_create_post` once per platform with the platform-specific caption variant.
6. For TikTok, always set `isAiGenerated: true`.
7. Confirm scheduled time and post IDs back to the user.
8. Log the post to the content log (see logging section below).

## Error handling

If a post fails:

1. Read the error message returned by Blotato.
2. Most common failures: media URL not reachable, account disconnected, character limit exceeded for platform.
3. Report the specific failure to the user with a fix suggestion.
4. Never silently retry. Always surface the error and let the user decide.

## Content logging

After every successful post, append a row to the content log (Google Sheet or local CSV):

| Date | Platform | Pillar | Caption preview | Image URL | Post URL | Scheduled time | Status |

This log feeds the Phase 3 skill-evolution-loop (caption performance scoring) once enough data accumulates.

## Approval workflow integration

When this skill is triggered by Sevyn AI via Telegram approval flow:

1. The Telegram message includes a selection code like "2B post 7am tuesday."
2. Parse: image index 2, caption option B, schedule for next Tuesday 7am Pacific.
3. Pull the image from the Higgsfield generation set, the caption from the API response set.
4. Confirm platform (default to user's last preference, ask if ambiguous).
5. Execute the posting flow above.
6. Reply to Sevyn confirming the post is queued.

## References

See `references/hashtags.json` for machine-readable hashtag sets used by automation.
See `references/posting-schedule.md` for content cadence and weekly rhythm guidance.

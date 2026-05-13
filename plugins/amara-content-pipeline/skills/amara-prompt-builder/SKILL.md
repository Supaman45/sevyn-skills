---
name: amara-prompt-builder
description: Construct Higgsfield Soul 2.0 image generation prompts for Amara with her trained Soul ID locked in. Use whenever the user wants to generate, create, batch, or queue images of Amara, design her content, or build a content batch for her social pipeline. Always trigger when image generation is needed for Amara, even if the user phrases it as "make me a photo of her" or "shoot something for the feed."
---

# Amara Prompt Builder

Builds Soul 2.0 image generation prompts that maintain Amara's face consistency, aesthetic, and brand positioning.

## Required context every prompt needs

Every Soul 2.0 generation for Amara assumes:

1. Soul ID for Amara is selected as the Character in the Higgsfield Character tab.
2. Aspect ratio defaults to 9:16 for reels and stories, 1:1 for feed posts, 4:5 for carousels.
3. Generations run in "fast" quality for first passes, switch to "high" only after composition is locked.

The skill outputs the prompt body only. The Soul ID selection and aspect ratio are set in the Higgsfield UI separately.

## The four content pillars

Every Amara image fits one of these pillars. Always identify the pillar before writing the prompt.

### Pillar 1, Morning Protocol
Subject matter: red light therapy, supplements being taken, morning mobility, journaling, matcha or coffee ritual, Oura ring checks, sunlight exposure.
Setting: bedroom, kitchen, bathroom, balcony or backyard at dawn.
Lighting: warm window light, golden hour east-facing, soft overhead.

### Pillar 2, Protocol Education
Subject matter: flat-lays of supplements with hand visible, journal pages, screen recordings of wearable data, books and printed research.
Setting: desk, counter, linen sheets, neutral textured surfaces.
Lighting: overhead natural, soft window-side.

### Pillar 3, Recovery Rituals
Subject matter: sauna, cold exposure, foam rolling, Epsom bath, breathwork on mat, infrared red light panel, walking pod sessions.
Setting: home spa, gym, bathroom, outdoor coastal walk, mat in bedroom.
Lighting: warm dim for evening rituals, harsh bright for cold exposure, golden for outdoor.

### Pillar 4, Wearable Data and Training
Subject matter: home pilates, light strength sets, Oura ring close-ups, Whoop on wrist, CGM on arm, post-workout glow.
Setting: home gym, living room with mat, kitchen during recovery meal.
Lighting: natural daylight, slight backlight, post-workout flushed skin.

## The aesthetic anchors

Amara's visual identity stays consistent across pillars. Every prompt should preserve at least three of these:

- Linen, oat, cream, sage palette (no neon, no black-and-white minimalism, no high contrast)
- Natural unposed framing (slight tilts, hand in frame, candid expressions)
- Phone-shot capture quality (slightly soft focus, real-world lighting imperfections)
- Subtle everyday makeup (tinted lip balm, light mascara, glowy skin)
- College-girl-cute energy (early 20s, fresh-faced, soft smile or candid expression)
- Optional: gold grills as occasional contrast accessory (1 in 5 posts max, never in pure wellness moments)

## The amateur phone aesthetic

Always add at least two of these phrases to push away from studio-perfect output:

Camera language: "iPhone photo," "front camera selfie," "candid phone snap," "mirror selfie with phone visible," "shot on iPhone."
Quality cues: "slightly soft focus," "natural grain," "no flash," "phone compression," "warm filter," "soft beauty filter," "VSCO warm tone."
Composition: "tilted slightly," "not centered," "casual framing," "hand in frame," "mid-movement."

## The college-girl-cute calibration

Default makeup language for every prompt:

"subtle everyday makeup, tinted lip balm, light brown mascara, glowy skin, no-makeup makeup look"

Dial up for evening or going-out content:
"defined eye, glossy lip, slight contour, dewy highlighter"

Dial down for raw morning or post-workout:
"bare face, tinted SPF only, slight freckles visible"

## The prompt template

Every Amara generation prompt follows this structure:

```
[capture style] [shot type] [setting], [outfit description], [face and makeup detail], [hair detail], [pose or action], [lighting], [filter or quality cue], [optional mood word]
```

### Example, Pillar 1 morning protocol:

"iPhone selfie in bed, just woke up, oversized linen pajama top, no-makeup makeup look with tinted lip balm, hair in messy waves over shoulder, holding Oura ring up to camera, soft morning window light from left, warm filter, sleepy smile"

### Example, Pillar 2 protocol education:

"candid phone photo overhead of bathroom counter, hand with neutral manicure holding magnesium glycinate capsules, amber supplement bottles and glass of water around it, wooden tray and linen towel, overhead natural light, slight VSCO warm tone, intimate documentary framing"

### Example, Pillar 3 recovery ritual:

"phone selfie in front of red light therapy panel, face half-lit in red glow, subtle glowy makeup, linen robe loosely tied, hair in low messy bun, soft smile, dark bedroom background, grainy low-light phone quality, intimate framing"

### Example, Pillar 4 wearable data and training:

"phone selfie sitting on yoga mat after pilates session, white sports bra and cream shorts, light flush on cheeks, hair in claw clip half-up, light mascara, home living room with plants visible, natural window light, soft skin filter, playful candid expression"

## When using Multi Reference

If the user wants to recreate a specific Pinterest or Instagram inspo image with Amara's face:

1. Upload the inspo image as a composition or style reference in Soul 2.0.
2. Keep Amara's Soul ID locked as the Character.
3. Write the prompt describing only what should change from the inspo (outfit, setting if different, mood).
4. Do not describe Amara's face in the prompt. Soul ID handles that.

## When adding props

If the prompt includes a specific product (Oura ring, Whoop band, supplement bottle, branded clothing):

1. Upload a clean image of the product as a Multi Reference input.
2. Reference it in the prompt by name: "Oura ring visible on hand" or "Whoop 4.0 on left wrist."
3. The model pulls the prop from the reference, not from training data.

## Batch generation note

When batching multiple prompts (5 or more for a content drop), vary across all four pillars and across all three calibration levels (bare face, college-cute default, evening dial-up). Never generate a batch with only one pillar represented unless the user specifies "all from pillar X."

## Output format

When asked to generate prompts, return them numbered, with the pillar labeled, ready to paste into Soul 2.0. Include a one-line note on intended use (feed post, reel first frame, carousel slide, story).

Example output:

```
1. Pillar 1 Morning Protocol, intended for IG feed post:
[full prompt here]

2. Pillar 3 Recovery Ritual, intended for reel first frame:
[full prompt here]
```

## References

See `references/pillars.md` for expanded pillar examples and visual moodboard descriptors.
See `references/prompt-templates.md` for additional template variants and edge cases.

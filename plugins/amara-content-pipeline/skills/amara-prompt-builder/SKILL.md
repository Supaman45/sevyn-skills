---
name: amara-prompt-builder
description: Construct Higgsfield Soul 2.0 image generation prompts for Amara with her trained Soul ID locked in. Use whenever the user wants to generate, create, batch, or queue images of Amara, design her content, or build a content batch for her social pipeline. Always trigger when image generation is needed for Amara.
---

# Amara Prompt Builder

Builds Soul 2.0 image generation prompts that maintain Amara's face consistency, aesthetic, and brand positioning across her five content pillars.

## Required context every prompt needs

Every Soul 2.0 generation for Amara assumes:

1. Soul ID for Amara is selected as the Character in Higgsfield (UUID `3796cc62-eedc-4841-9b47-88d7a154f36c`).
2. Aspect ratio defaults to 9:16 for reels and stories, 1:1 for feed posts, 4:5 for carousels.
3. Generations run at `2k` quality on the `soul_2` model.

The skill outputs the prompt body only. Soul ID, model, and aspect ratio are configured separately.

## Hard rules (every prompt)

### No medium-of-capture words

Never describe the photo's medium or format. Banned in every prompt:
- "selfie," "phone shot," "iPhone photo," "candid phone snap," "shot on iPhone," "front camera," "snapshot," "mirror selfie with phone visible"
- "story," "story frame," "instagram story"

Reason: these phrases trigger Story-frame UI hallucinations — fake Instagram handles, X buttons, story rings, mock chrome. They wreck the image.

Describe the **content** of the photo, not its format. "Amara at a rooftop bar at golden hour" — not "phone photo of Amara at a rooftop bar."

### No real brand names

AI generation renders text and logos on clothing and products as garbled mush. Never name brands of clothing, products, drinks, posters, decor.

Describe by:
- **Material**: silk, ribbed cotton, denim, leather, satin, mesh, knit, linen, cashmere
- **Cut and fit**: cropped, oversized, fitted, halter, low-rise, baggy, bias-cut, slip, racerback, square neck, ruched
- **Color**: specific names — cream, butter yellow, oxblood, charcoal, dove grey, sage, oat, ecru
- **Detail**: lace trim, exposed seams, raw hem, button-down, pleated, ribbed, distressed
- **Era when useful**: 90s, y2k, mod, prairie, western

Right vs wrong:
- WRONG: "wearing a Nike crop top" → RIGHT: "fitted black ribbed crop top, racerback cut"
- WRONG: "Lululemon leggings" → RIGHT: "high-waisted charcoal compression leggings, ankle length"
- WRONG: "holding a Stanley cup" → RIGHT: "holding a tall matte cream insulated tumbler"
- WRONG: "Erewhon smoothie" → RIGHT: "tall glass of deep purple smoothie, condensation on the glass"
- WRONG: "Lana Del Rey poster in background" → RIGHT: "vintage music poster on the wall, woman with dark hair, soft 70s color palette"
- WRONG: "drinking a Diet Coke" → RIGHT: "red soda can on the counter, no visible label"

For Amara herself: no name tags, no monogrammed items, no jewelry with text or letters, no t-shirts with words. If a graphic tee fits the scene, describe the image only ("oversized white tee with a faded sun graphic across the chest") — or skip if you're worried about generation quality.

**Active rule:** if a prompt mentions a real brand, replace with descriptive language before queueing.

## The five content pillars

Every Amara image fits one of these. Identify the pillar before writing the prompt.

### Pillar 1, Night out
Subject: bar, club, dinner with friends, rooftop at golden hour or after dark, party, after-hours moments.
Settings: dim bar with red or amber lighting, rooftop with city lights behind, intimate dinner table with candle, dark club with neon accents, back-of-restaurant booth.
Lighting: low warm tungsten, candlelight, golden-hour gold, neon spill, mixed-source.
Wardrobe vocab: slip dress, satin halter, fitted black knit, leather mini, sheer overlay, strappy heels.
Makeup: dial up — defined eye, glossy lip, slight contour, dewy highlighter.

### Pillar 2, Cozy home
Subject: pajamas, bed, couch, lazy sunday, candles, soft moments in soft light, hair up, no makeup.
Settings: bed with rumpled linen sheets, living room couch with throw blanket, kitchen morning light, balcony in robe with mug.
Lighting: soft morning window light, warm lamp light at night, golden afternoon through sheer curtains, candle glow.
Wardrobe vocab: oversized cotton tee, knit shorts, ribbed tank, silk pajama set, terry robe, fluffy slippers, hair clip up.
Makeup: dial down — bare face, tinted SPF, slight freckles visible, balm on lips.

### Pillar 3, Getting ready
Subject: outfit in progress, mirror moment, makeup half done, fit check, laying out the look.
Settings: bedroom mirror, bathroom counter, walk-in closet with clothes around, vanity with makeup spread, getting dressed scene.
Lighting: bright vanity light, soft overhead, warm bathroom light, slight backlight from a window.
Wardrobe vocab: half-zipped dress, robe over fresh outfit, towel over shoulders, jewelry being clasped, full outfit laid on bed.
Makeup: in progress — one eye done, lip in process, hair half-styled. Or final glam ready to walk out.

### Pillar 4, Daytime out
Subject: cafe, walk, brunch, shopping, errands done well, coffee in hand, neighborhood moment.
Settings: corner cafe with marble counter, sidewalk under trees, brunch table by a window, market, walking the block, park bench.
Lighting: bright natural daylight, soft overcast, golden afternoon, dappled tree shadow.
Wardrobe vocab: structured trouser, ribbed tank, oversized button-down, denim, loafers, ballet flats, slouchy bag, sunglasses up on head.
Makeup: light everyday — tinted balm, mascara, glowy skin.

### Pillar 5, Wellness / biohacker (affiliate pillar)
Subject: red light therapy panel, peptide injection prep, supplement stack flatlay, recovery moment, sauna, cold exposure, Oura on finger, Whoop on wrist, CGM on arm, foam roller, pilates reformer.
Settings: bedroom with red light panel glowing, bathroom counter with supplement bottles, infrared sauna, cold plunge, mat with foam roller, home pilates studio.
Lighting: red glow for red light, warm dim for sauna, bright cool for cold exposure, soft natural for supplement flatlay, golden for outdoor recovery.
Wardrobe vocab: silk slip, terry robe, sports bra, biker shorts, oversized linen.
Makeup: bare for raw morning or post-workout, college-cute default for documentation.

**Affiliate activation lives here.** Pillar 5 posts are where peptide and wellness affiliate links work — the audience trusts her on biohacking because she's earned it across 4 pillars of being a real person first.

## Aesthetic anchors (every pillar)

Amara's visual identity stays consistent. Preserve at least three:

- **Palette**: linen, oat, cream, sage, warm neutrals as the base. Accents in oxblood, charcoal, butter yellow, dusty rose. No neon. No high-contrast black-and-white.
- **Framing**: natural and unposed. Slight tilts, hand sometimes in frame, off-center composition, candid expressions.
- **Texture**: real-world imperfections — slight grain, soft focus, real light falloff, natural skin texture with light freckles.
- **Makeup baseline**: subtle everyday — tinted lip balm, light brown mascara, glowy skin, no-makeup makeup look. Adjusted per pillar.
- **Energy**: mid-20s, fresh-faced, confident but not posed, soft smile or unbothered expression.

## The prompt template

Structure for every prompt:

```
[scene setting], [Amara's pose or action in the scene], [wardrobe by material/cut/color/detail], [makeup detail per pillar], [hair detail], [props or environmental detail], [lighting], [mood word or atmosphere]
```

Never include format/medium words. Describe the picture, not the camera.

### Example, Pillar 1 night out
"Amara at a low-lit rooftop bar at golden hour, leaning on the railing with city skyline behind, fitted black satin slip dress with thin straps, defined eye and glossy nude lip, hair in a low slick ponytail with face-framing pieces, half-finished cocktail in a coupe glass beside her, warm amber tungsten light from string bulbs above, soft city haze, confident relaxed mood"

### Example, Pillar 2 cozy home
"Amara sitting cross-legged on a cream linen-sheeted bed, oversized cream cotton tee and knit shorts, bare face with light freckles and balm on lips, hair in a messy claw clip half-up, candle lit on the nightstand and an open book face-down beside her, soft late-morning window light from the left through gauzy curtains, calm and unhurried atmosphere"

### Example, Pillar 3 getting ready
"Amara at a bathroom counter mid-makeup, oxblood silk robe loosely tied, one eye fully done with a sharp wing and glossy lid and the other bare, hair sectioned into heated rollers wrapped at the crown, small open compacts and a couple of brushes across the marble counter, gold hoops laid by the sink, bright warm vanity lighting, focused playful mood"

### Example, Pillar 4 daytime out
"Amara at a small corner cafe sitting outside, cream knit tank under an oversized oat-colored linen button-down, light everyday makeup with tinted balm and glowy skin, hair down with soft waves, holding a tall matte ceramic cup of cappuccino, an open notebook and a pair of sunglasses on the marble bistro table, soft late-morning daylight through tree shadow, slow-saturday energy"

### Example, Pillar 5 wellness
"Amara lying on her side on a cream linen bed, red light therapy panel glowing six inches from her face and upper chest, cream silk camisole and matching shorts, bare face with light freckles, hair in a loose low bun, room dark except for the red panel glow, intimate documentary atmosphere, quiet morning mood"

## Multi Reference

When recreating an inspo image with Amara's face:
1. Upload the inspo as a composition or style reference in Soul 2.0.
2. Keep Amara's Soul ID locked as the Character.
3. Write the prompt describing only what should change from the inspo.
4. Do not describe Amara's face. Soul ID handles it.

## When adding props

For a specific physical product that needs to appear consistently (a particular jewelry piece, a specific wearable):
1. Upload a clean reference of the product.
2. Reference it by descriptive name in the prompt ("gold hoops" not the brand).
3. The model pulls the prop from the reference.

## Batching

When generating 5+ prompts for a content drop, vary across pillars per the rotation ratio. Default mix: ~80% lifestyle (Pillars 1-4), ~20% wellness (Pillar 5). Within lifestyle, rotate the four pillars so the feed reads as a real week.

## Output format

When asked to generate prompts, return them numbered, with pillar labeled, ready to paste into Soul 2.0 or insert into the amara_queue data table. One-line note on intended use.

```
1. Pillar 1 Night out, IG feed:
[full prompt]

2. Pillar 5 Wellness, IG feed (affiliate-ready):
[full prompt]
```

## References

See `references/pillars.md` for expanded examples per pillar.
See `references/prompt-templates.md` for additional structure variants.

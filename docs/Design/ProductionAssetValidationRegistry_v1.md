# Production Asset Validation Registry v1

## Purpose

Track current cat art validation assets and prevent candidate resources from being confused with approved runtime sprites.

This registry is for production art validation only. It does not change gameplay, Behavior, Growth, Reveal, Save, or Desktop Foundation.

## Asset Status Levels

### Level 0 - Raw AI / Source Sheet

Original generated image or sprite sheet.

Use for reference and reprocessing only.

Not directly used by runtime.

### Level 1 - Processed Validation Frames

Frames cleaned, split, centered, or converted to transparent PNG for Godot preview.

Use for visual validation inside the real desktop pet window.

Not approved as final runtime art.

### Level 2 - Candidate Approved For Motion Direction

Motion direction has passed manual validation in the real Godot desktop runtime.

The asset should preferably match the current main cat identity, but exact identity match is not required at Level 2.

May still require hand cleanup, consistent transparency, or final redraw.

Not yet promoted to runtime sprite folders.

### Level 3 - Runtime Candidate

Frames are ready to copy into:

```text
assets/characters/cat/sprites/<behavior>/
```

Still requires final validation in normal runtime mode.

### Level 4 - Runtime Approved

Frames are active production runtime sprites.

## Current Character Baseline

### Main Cat - Front Sit

Status: Level 2 - Candidate Approved For Motion Direction

Current preview frames:

```text
assets/characters/cat/production/character_master_front_sit_preview/
```

Source and processed reference:

```text
assets/characters/cat/production/character_master_front_sit/
```

Assessment:

- Main cat identity is acceptable.
- Warm brown tabby direction is acceptable.
- One-meter readability passes.
- Original AI output did not provide true transparency.
- Current transparent version is post-processed and suitable for validation.
- Not final runtime art.

Known issues:

- Minor edge artifacts may remain from fake-background removal.
- Future final art should be exported with real alpha transparency.

## Current Idle / Breathing Validation

### Idle Breath AI v2

Status: Level 2 - Candidate Approved For Motion Direction

Current frames:

```text
assets/characters/cat/production/idle_breath_ai_v2/
```

GIF preview:

```text
assets/characters/cat/production/gif_previews/idle_breath_ai_v2.gif
```

Source sheet:

```text
assets/characters/cat/production/sheets/idle_breath_ai_v2_source.png
```

Assessment:

- Character consistency passes.
- One-meter readability passes.
- Low-interruption requirement passes.
- Breathing motion is valid but subtle.

Known issues:

- Breathing amplitude is weak.
- Original AI output did not provide true transparency.
- Use as validation-level asset only.

Recommended next art revision:

- Keep the same character.
- Increase frame 02 chest/body breathing amplitude by roughly 20% to 30%.
- Keep feet, tail, face, eyes, and overall position stable.

## Current Sleep / Breathing Validation

### Sleep Breath AI v1

Status: Level 2 - Candidate Approved For Motion Direction

Current frames:

```text
assets/characters/cat/production/sleep_breath_ai_v1/
```

GIF preview:

```text
assets/characters/cat/production/gif_previews/sleep_breath_ai_v1.gif
```

Source frames:

```text
assets/characters/cat/production/sheets/sleep_breath_ai_v1_sources/
```

Assessment:

- Sleep pose direction is acceptable for validation.
- Character identity is broadly compatible with the current main cat.
- Three-frame order is normal sleep, inhale, return to normal sleep.
- Frames were post-processed from fake checkerboard background into transparent PNG.
- Godot runtime launch validation passed with this preview target.
- Player manual runtime validation passed.

Known issues:

- Original AI output did not provide true transparency.
- Frame-to-frame markings and body volume should be checked in real desktop scale.
- Not yet promoted to runtime sprite folders.

## Current Head Tilt Validation

### Head Tilt Best Candidate v1

Status: Level 1 - Processed Validation Frames / Rejected For Head Tilt

Current frames:

```text
assets/characters/cat/production/head_tilt_best_candidate_v1/
```

Review frames:

```text
assets/characters/cat/production/head_tilt_ai_review/
```

Review GIF:

```text
outputs/art_preview_debug/head_tilt_review/head_tilt_best_candidate_v1.gif
```

Assessment:

- Best current candidate for front-facing head tilt.
- Built from the `7001` three-frame output.
- Frame order is left tilt, center, right tilt, center.
- Godot runtime launch validation passed with this preview target.
- Not yet approved as Level 2.
- Rejected as a normal cat head-tilt motion because the body also leans/rotates too much.

Known issues:

- Only three unique poses exist; no true in-between frames.
- Body silhouette shifts more than ideal.
- Cat identity is orange-tabby adjacent but not the current main cat.
- Keep as cute pose reference only; do not promote as head tilt motion.

### AI Head Turn / Pose Review Batch

Status: Level 1 - Processed Review Frames

Review frames:

```text
assets/characters/cat/production/head_tilt_ai_review/
```

Recombined review GIFs:

```text
outputs/art_preview_debug/recombined_action_review/
```

Assessment:

- Several generated sheets failed the intended front-facing head-tilt requirement.
- Some frames are useful for other future motion directions.
- `view_turn_mix_7476` is the best candidate for a future front-to-back turn-around reference.
- `view_turn_mix_4297` contains a possible back-facing idle/tail reference.
- `front_idle_static_9300` is mostly static and may be used only as a front-sit reference.

Known issues:

- Most recombined candidates are not Level 2.
- `tilt_turn_mixed_9861` was promoted separately as Curious Body Lean Candidate v1.
- Character identity differs from the current main cat.
- Several sheets contain cropped edge artifacts from source-sheet splitting.

## Current CuriousLean Validation

### CuriousLean Candidate v1

Status: Level 2 - Candidate Approved For Motion Direction

Current frames:

```text
assets/characters/cat/production/curious_lean_candidate_v1/
```

GIF preview:

```text
assets/characters/cat/production/gif_previews/curious_lean_candidate_v1.gif
```

Source review frames:

```text
assets/characters/cat/production/head_tilt_ai_review/tilt_turn_mixed_9861/
```

Assessment:

- Motion direction passed player manual review as a cute curious body-lean action.
- This is not a normal head-only tilt.
- Body movement is acceptable because the action is classified as whole-body curious lean.
- Slow playback is required for the action to feel calm and low-interruption.
- The left-up and right-up poses must hold for roughly two seconds each.
- Current preview sequence uses repeated frames to create timing holds instead of changing runtime animation logic.
- Current rhythm is left hold, transition, center, right hold, center, transition.

Cleanup notes:

- Original raw six-frame source remains archived under `assets/characters/cat/production/curious_lean_candidate_v1_base_raw/`.
- Clean base frames are rebuilt under `assets/characters/cat/production/curious_lean_candidate_v1_base/`.
- Current 28-frame preview sequence is rebuilt from the clean base frames.
- Edge fragments from adjacent source-sheet cats were removed by keeping the main cat body per frame.
- The GIF preview was regenerated after cleanup.
- Foot/lower-body anchor stabilization was applied after cleanup to reduce synchronous limb sliding.
- The stabilized frames use extra transparent side padding to avoid cropping during alignment.

Known issues:

- Character identity differs from the current main cat.
- Not yet promoted to runtime sprite folders.
- Should not be reused as a head-only tilt reference.

## Historical / Reference Validation Assets

### Legacy Breathing

Status: Level 1 - Processed Validation Frames

Path:

```text
assets/characters/cat/production/breathing/
```

Assessment:

- Earlier breathing validation.
- Different visual generation pass from the current main cat.
- Keep as process reference only.

### Back View / Tail Motion

Status: Level 2 - Candidate Approved For Motion Direction

Path:

```text
assets/characters/cat/production/cock_its_head_back/
```

GIF preview:

```text
assets/characters/cat/production/gif_previews/cock_its_head_back.gif
```

Source sheet:

```text
assets/characters/cat/production/sheets/cock_its_head_back.png
```

Assessment:

- Resource still exists.
- Back-facing silhouette and tail motion passed manual runtime validation.
- Color palette and tabby markings are broadly compatible with the current main cat.
- Not guaranteed to be the exact same cat identity.
- Keep as back-view/tail-motion reference.

Known issues:

- Needs identity comparison against the final main cat before Level 3 or Level 4 promotion.
- Should not be used as official runtime art yet.

### Catwalk

Status: Level 1 - Processed Validation Frames

Path:

```text
assets/characters/cat/production/catwalk/
```

Source sheet:

```text
assets/characters/cat/production/sheets/catwalk.png
```

Assessment:

- Motion validation only.
- Contains mixed line/color frame quality.
- Not aligned enough with current main cat for direct promotion.

### Head Shake / Yaotou

Status: Level 1 - Processed Validation Frames

Paths:

```text
assets/characters/cat/production/yaotou/
assets/characters/cat/production/yaotou_loop/
assets/characters/cat/production/yaotou_smooth_color/
```

Source sheet:

```text
assets/characters/cat/production/sheets/yaotou.png
```

Assessment:

- Useful for direction and sequence validation.
- Corrected loop direction exists.
- Auto-smoothed/colorized version is preview-only.
- Not suitable as final art.

## Current Runtime Sprite Folder

Runtime sprite path:

```text
assets/characters/cat/sprites/
```

Current approved/active production runtime status:

- Idle has early production runtime frames.
- Walk, sit, and sleep are not fully production-approved.
- Candidate validation folders under `production/` are not automatically runtime-approved.

## Current Art Preview Target

Configured in:

```text
config/art_preview.cfg
```

Current target:

```text
assets/characters/cat/production/idle_breath_ai_v2/
```

Preview mode should be used for candidate validation only.

## Promotion Rule

A candidate asset may be promoted only when:

- It matches the current main cat identity.
- Its motion has already passed Level 2 manual runtime validation.
- It uses true transparent PNG or has clean post-processed transparency.
- It passes one-meter readability.
- It has stable canvas size and anchor.
- Motion is low-interruption.
- It does not introduce gameplay, Behavior, Growth, Reveal, or Save changes.

After promotion, copy frames into:

```text
assets/characters/cat/sprites/<behavior>/
```

Then disable art preview mode and validate in normal runtime.

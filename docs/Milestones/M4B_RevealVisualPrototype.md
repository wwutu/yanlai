# M4-B Phase 1 Reveal Visual Prototype

## Reveal Visual Approach

The first Reveal visual prototype uses a conservative sprite modulation approach.

CatLayer renders the active Validation Cat sprite with:

- a soft muted base shape at low Reveal
- increasing full-color sprite opacity as Reveal increases
- a gentle warm overlay derived from Reveal

The visual is continuous and derived from the existing RevealSystem output.

## Implemented

- Reveal is visually affected by Growth through RevealSystem.
- Low Growth displays the Validation Cat as less fully revealed.
- High Growth displays the Validation Cat as more complete and warm.
- The effect is applied directly to Validation Cat sprites.
- The effect remains large-area, soft, and readable at desktop scale.

## Intentionally Not Implemented

- Final Reveal art
- Hard-edged masks
- Random scattered patches
- Milestone animation
- Celebration effects
- Particles
- Sound
- UI changes
- Growth ownership changes
- Reveal ownership changes
- Behavior logic changes
- Save changes

## Validation Result

- Project loads in Godot 4.7.
- Validation Cat sprites load successfully.
- Reveal changes visually with Growth.
- Reveal remains derived from Growth.
- Reveal is not saved.
- Behavior remains unchanged.
- Runtime chain remains unchanged: Desktop Time to Growth to Reveal to Render.
- The current effect avoids disease, dirt, damage, baldness, or broken visual impressions.

## Known Limitations

- This is prototype Reveal presentation only.
- The effect uses whole-sprite modulation, not final region-based reveal art.
- Production Reveal visual design remains future work.

# Reveal Prototype Implementation Review

## Implementation Method

The current Reveal Visual Prototype uses sprite modulation and alpha blending.

CatLayer draws the current Validation Cat sprite multiple times:

- muted low-opacity base shape
- full-color sprite layer with opacity increasing as Reveal increases
- soft warm overlay layer with opacity increasing as Reveal increases

The effect uses:

- tint
- opacity
- overlay through repeated sprite drawing
- alpha blending

The effect does not use:

- shader
- mask
- random patch system
- particle system
- production reveal art

## Data Source

The Reveal visual reads from RevealSystem through `get_reveal_percentage()`.

RevealSystem derives Reveal from Growth.

Reveal is not saved.

SaveSystem persists only:

- Growth
- Desktop Time
- Last Exit Time

## Visual Behavior

### Low Growth

The cat appears as a softer, muted, less complete silhouette.

The full-color layer is present but low opacity.

### Medium Growth

The cat becomes more readable.

The full-color layer becomes stronger and the warm Reveal layer becomes noticeable.

### High Growth

The cat appears mostly complete.

The full-color layer is strong and the warm Reveal layer remains gentle.

## Prototype Limits

This implementation is temporary.

It is:

- placeholder visual
- not final art
- not final reveal mask
- not final production shader
- not final region-based reveal presentation
- not milestone animation
- not production VFX

## Visual Safety

The current effect avoids:

- disease-like patches
- dirty look
- broken sprite look
- harsh random spots
- noisy scattered reveal
- overly flashy effects

The effect is large-area and continuous instead of patch-based.

## Screenshot or Capture

Screenshots were not created during this documentation review.

Reason:

- This phase is documentation and inspection only.
- No runtime, asset, scene, or configuration changes were required.
- Captures should be created later as explicit validation artifacts if needed.

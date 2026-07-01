# M4-A Phase 1 Validation Cat Asset Integration

## Objective

Establish the asset pipeline for the Validation Cat. Integrate reference images as the official frozen reference. Document the rendering pipeline and planned replacement workflow.

## Reference Assets

### Imported Files

- `assets/references/cat/validation_cat_form_reference_v1.png`
- `assets/references/cat/validation_cat_master_pose_v1.png`

### Asset Purpose

These files serve as:

- The official frozen visual reference for the Validation Cat
- The canonical source reference for Validation Cat pose extraction is `validation_cat_master_pose_v1.png`
- The source of truth for sprite creation in later phases
- The master pose reference for animation rigging

### Character Form Reference

`validation_cat_form_reference_v1.png` defines shared character form only.

Character Form includes:

- Shared body proportion
- Silhouette
- Head shape
- Eye shape
- Ear shape
- Tail shape

Form is shared.

### Character Appearance

Character Appearance includes:

- Fur color
- Fur pattern
- Nose color
- Paw color
- Eye color

Appearance is replaceable.

`validation_cat_form_reference_v1.png` is not the permanent appearance reference.

### Master Pose Reference

`validation_cat_master_pose_v1.png` is the canonical pose extraction reference.

Master Pose is the source reference for validation sprite extraction.

Runtime uses extracted validation sprite assets after M4-A Phase 4.

### Asset Status

FROZEN. These files must not be modified or renamed.

## Directory Structure

```
assets/
├── references/
│   └── cat/
│       ├── validation_cat_form_reference_v1.png
│       └── validation_cat_master_pose_v1.png
├── validation/
│   └── sprites/
└── production/
```

### Directory Purpose

- `references/` - Frozen reference assets (source of truth)
- `validation/` - Validation-phase sprites (placeholder quality, used for testing)
- `production/` - Production-quality sprites (final art)

## Rendering Pipeline Analysis

### Previous Placeholder Rendering

Before M4-A Phase 2, the cat was rendered entirely through procedural drawing in `scripts/cat/cat_layer.gd`.

**Rendering entry point:** `CatLayer._draw()` method

**Drawing methods used:**
- `draw_arc()` - Head circle, ear outlines
- `draw_polyline()` - Body ellipse, tail, whiskers
- `draw_circle()` - Eyes, nose, tail tip
- `draw_line()` - Legs, closed eyes (sleep), whiskers
- `draw_colored_polygon()` - Reveal color regions (body fill, ear fill, chest fill)

This procedural line-cat draw path is no longer active after M4-A Phase 2.

### Rendering Entry Point

`CatLayer._draw()` is called every frame via `queue_redraw()`. The draw method reads:

1. `_get_current_behavior_id()` - Determines pose (idle/walk/sit/sleep)
2. `_validation_textures` - Loaded validation sprite assets
3. `_reveal_system.get_reveal_percentage()` - Reveal placeholder tint

### Resource Loading Path

Current runtime loading path:
```
CatLayer._ready()
  loads assets/validation/sprites/cat/<behavior>.png
      draws texture in CatLayer._draw()
```

### Replacement Status

| Previous Element | Replacement Source | Status |
|----------------|-------------------|-------|
| Body ellipse | Validation sprite asset | Replaced in M4-A Phase 4 |
| Head circle | Validation sprite asset | Replaced in M4-A Phase 4 |
| Ear triangles | Validation sprite asset | Replaced in M4-A Phase 4 |
| Tail polyline | Validation sprite asset | Replaced in M4-A Phase 4 |
| Leg lines | Validation sprite asset | Replaced in M4-A Phase 4 |
| Eye circles | Validation sprite asset | Replaced in M4-A Phase 4 |
| Reveal color fills | Derived tint over Validation Cat | Placeholder |

### Placeholder Status

The procedural line art is no longer the active rendering method.

Validation sprite assets are active at runtime.

Reveal presentation remains placeholder.

## Planned Replacement Workflow

### Asset Pipeline Flow

```
Reference Assets (frozen)
    ↓
Validation Sprites (placeholder quality, testable)
    ↓
Production Sprites (final art)
```

### Replacement Strategy

1. Validation sprites are extracted from reference images
2. Each behavior (idle/walk/sit/sleep) has a corresponding sprite asset
3. CatLayer now loads and displays validation sprite assets instead of procedural drawing or runtime sheet cropping
4. Reveal overlay will be applied on top of sprites
5. Production sprites will replace validation sprites in the same locations

### Files That Will Be Modified

- `scripts/cat/cat_layer.gd` - Loads validation sprite assets directly
- `assets/validation/sprites/cat/` - Contains validation sprite assets
- `assets/production/` - Will contain production sprite frames

### Files That Will NOT Be Modified

- `scripts/cat/behavior_system.gd` - Behavior logic unchanged
- `scripts/cat/cat_brain.gd` - Selection logic unchanged
- `scripts/cat/cat_behavior.gd` - Behavior data unchanged
- `scripts/runtime/*` - All runtime systems unchanged

## Validation Results

- Project loads in Godot 4.7.
- No runtime regression.
- No behavior regression.
- Asset directories created correctly.
- Reference images accessible at `assets/references/cat/`.
- No runtime system changed.
- Validation Cat runtime rendering active.

## Explicitly Not Implemented

- Animation frames
- Production art
- Behavior logic changes
- Runtime system changes

# M4-A Phase 2 Validation Cat Runtime Integration

## Runtime Integration

- Validation Cat is now active at runtime.
- At this phase, CatLayer loaded `assets/references/cat/validation_cat_master_pose_v1.png`.
- At this phase, runtime textures were generated from the frozen reference image.
- Original reference artwork is not modified.
- Procedural line-cat rendering has been removed from the active CatLayer draw path.
- BehaviorSystem remains unchanged.
- GrowthSystem remains unchanged.
- RevealSystem remains unchanged.

## Behavior Rendering Verification

- Idle renders with Validation Cat reference artwork.
- Walk renders with Validation Cat reference artwork.
- Sit renders with Validation Cat reference artwork.
- Sleep renders with Validation Cat reference artwork.
- Behavior timing remains unchanged.
- Behavior selection remains unchanged.

## Rendering Verification

- Runtime-generated Validation Cat textures are scaled inside the existing desktop pet window.
- Rendering stays within the 220x220 window bounds.
- Runtime transparency is generated from the light reference background.
- No clipping was detected by validation.
- No runtime scaling outside the expected one-meter desktop footprint was detected.

## Reveal Rendering Status

PLACEHOLDER.

Reveal remains derived from Growth and is still read by CatLayer.

Current runtime rendering applies a simple derived reveal tint over the Validation Cat sprite. This verifies that Reveal still reaches Render, but it is not final production reveal presentation.

## Remaining Placeholder Assets

NONE for active cat rendering.

The remaining placeholder status is Reveal presentation, not the Validation Cat artwork.

## Validation Results

- Project loads in Godot 4.7.
- Validation Cat runtime textures load successfully.
- Runtime-generated transparent pixels are present.
- Rendering scale remains inside the desktop window.
- Desktop Time to Growth to Reveal to Render chain still passes.
- Behavior remains valid and changes over time.
- Save data remains facts-only.
- No behavior logic was changed.
- No runtime system was changed.

# M4-A Phase 2.1 Validation Cat Pose Source Correction

## Previous Source

- `assets/references/cat/validation_cat_form_reference_v1.png`

The previous file was originally named `validation_cat_v1.png`.

## Corrected Source

- `assets/references/cat/validation_cat_master_pose_v1.png`

## Current Canonical Pose Reference

- `validation_cat_master_pose_v1.png`
- Corresponds to `VALIDATIONCATV1-MASTERPOSEEXPLORATIONV1.1`
- Current priority pose: IdleSit

## Validation Result

- Project loads in Godot 4.7.
- At this phase, Validation Cat runtime source was corrected to the Master Pose reference.
- Idle, Sit, Sleep, and Walk all generate valid runtime textures from the Master Pose source.
- BehaviorSystem was not modified.
- GrowthSystem was not modified.
- RevealSystem was not modified.
- SaveSystem was not modified.
- Runtime chain still passes: Desktop Time to Growth to Reveal to Render.
- Rendering scale remains inside the desktop window.
- One-meter Principle still passes for the current runtime validation scale.

# M4-A Phase 4 Validation Sprite Pipeline

## Validation Sprite Assets

Created:

- `assets/validation/sprites/cat/idle.png`
- `assets/validation/sprites/cat/walk.png`
- `assets/validation/sprites/cat/sit.png`
- `assets/validation/sprites/cat/sleep.png`

These sprites were extracted from:

- `assets/references/cat/validation_cat_master_pose_v1.png`

## Reference Asset Responsibility

Reference assets are frozen source references.

`validation_cat_master_pose_v1.png` remains the canonical Master Pose reference.

Runtime no longer depends on crop coordinates inside the Master Pose reference sheet.

## Sprite Asset Responsibility

Validation sprite assets are runtime-facing validation assets.

CatLayer loads the validation sprites directly from:

- `assets/validation/sprites/cat/`

## Runtime Update

- Runtime crop logic was removed from CatLayer.
- Runtime sheet coordinate dependency was removed.
- CatLayer now loads explicit sprite PNG files.
- Behavior timing was not changed.
- BehaviorSystem was not changed.
- GrowthSystem, RevealSystem, SaveSystem, and DesktopTimeSystem were not changed.

## Validation Result

- Project loads in Godot 4.7.
- Idle sprite loads.
- Walk sprite loads.
- Sit sprite loads.
- Sleep sprite loads.
- Sprite rendering stays inside the desktop window bounds.
- Runtime chain still passes: Desktop Time to Growth to Reveal to Render.
- Behavior remains valid and changes over time.
- Save data remains facts-only.

# M4-A Phase 2.2 Validation Asset Naming Standardization

## Renamed Asset

- From: `assets/references/cat/validation_cat_v1.png`
- To: `assets/references/cat/validation_cat_form_reference_v1.png`

## Naming Clarification

- `validation_cat_form_reference_v1.png` defines Character Form only.
- Character Form is shared.
- Character Appearance is replaceable.
- `validation_cat_master_pose_v1.png` remains unchanged.
- `validation_cat_master_pose_v1.png` is the canonical pose extraction reference.

## Runtime Verification

- At this phase, runtime still used `assets/references/cat/validation_cat_master_pose_v1.png`.
- `validation_cat_form_reference_v1.png` is not used directly by runtime.
- Project loads in Godot 4.7.
- No broken resource references were found.
- Rendering still passes.
- Behavior still passes.
- Reveal remains unchanged.

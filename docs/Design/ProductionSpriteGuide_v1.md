# Production Sprite Guide v1.0

## 1. Purpose

Production Sprite Guide v1.0 defines how Yanlai production sprite assets are created.

Its objective is consistency during production. Character exploration has already ended. Character Master has been frozen, and the three CMR Root States have been defined.

Sprite production is implementation rather than exploration.

This guide does not redefine Character Master, project philosophy, or project roadmap.

## 2. Relationship with Character Master

Character Master is the highest visual authority.

Every production sprite must inherit from one CMR Root State.

Sprite production must never redesign:

- Proportions
- Silhouette
- Facial language
- Character personality
- Companion feeling

If Character Master changes in the future, it must happen through an explicit Character Master revision rather than sprite production.

## 3. Three Root States

The three frozen Root States are:

### CMR001 - Rest Root

Source reference:

- `assets/character_master/CMR_001_Resting.png`

Used for:

- Idle
- Blink
- Ear movement
- Tail movement
- Normal breathing

### CMR002 - Relax Root

Source reference:

- `assets/character_master/CMR_002_Calm.png`

Used for:

- Relax
- Sleep transition
- Sleep
- Long resting state
- Low posture states

### CMR003 - Interaction Root

Source reference:

- `assets/character_master/CMR_003_Sitting.png`

Used for:

- Petting response
- Mouse interaction
- Head tilt
- Observe cursor
- Butterfly
- Furniture interaction
- Curious response

## 4. Sprite Canvas Standard

Current production target:

- 96 x 96 pixels
- Transparent background
- Consistent anchor point
- Stable feet position whenever applicable
- Stable shadow position
- Character centered consistently

These are production targets rather than artistic constraints.

## 5. One Meter Principle

The One Meter Principle is a mandatory validation rule.

Every production sprite must be evaluated primarily at actual runtime size.

Never approve sprites solely while zoomed in.

Validation focuses on:

- Readable silhouette
- Readable state
- Subtle life
- Low interruption

Micro movement should create presence rather than attract attention.

## 6. Sprite Consistency Rule

Every sprite should immediately be recognizable as the same Yanlai.

No production sprite may introduce:

- New proportions
- New face language
- New silhouette
- New personality

Sprite production extends Character Master.

It never redesigns Character Master.

## 7. Motion Principles

Motion principles are relative. This guide does not specify pixel values.

Breathing should primarily affect the chest and upper body rather than moving the entire body.

Blink should only affect the eyes.

Ear movement should remain subtle.

Tail movement should remain relaxed and infrequent.

Head tilt belongs only to the Interaction Root.

Sleep transitions should naturally evolve from the Relax Root.

Movement should support the companion feeling rather than performance.

## 8. Runtime First Rule

Final sprite approval is performed inside the actual runtime.

Large artwork is only a production aid.

The final visual judgment must always be based on the real desktop experience.

## 9. Asset Directory Standard

Production art uses separate directories for candidate work and runtime-ready sprites.

### Candidate / Validation Work

Use:

```text
assets/characters/cat/production/
```

This directory is for:

- animation validation
- candidate frames
- near-final experiments
- process exports
- sprite sheets before runtime extraction

Files in this directory are not considered the canonical runtime source.

### Runtime Sprites

Use:

```text
assets/characters/cat/sprites/<behavior>/
```

This directory is for sprites that Godot runtime is allowed to load directly.

Runtime frame naming:

```text
frame_01.png
frame_02.png
frame_03.png
```

Current behavior directories:

```text
assets/characters/cat/sprites/idle/
assets/characters/cat/sprites/walk/
assets/characters/cat/sprites/sit/
assets/characters/cat/sprites/sleep/
```

Validated candidate frames should be copied or exported into the runtime sprite directory before runtime approval.

### Sprite Sheet Rule

Sprite sheets may be stored under:

```text
assets/characters/cat/production/sheets/
```

The current runtime pipeline uses independent PNG frames, not sprite sheets.

Before runtime approval, sprite sheets should be exported into independent `frame_XX.png` files under `assets/characters/cat/sprites/<behavior>/`.

## 10. Production Checklist

Every production sprite should pass:

- Correct CMR Root selected
- Character Master preserved
- Silhouette preserved
- Companion feeling preserved
- One Meter Principle satisfied
- Runtime validation completed

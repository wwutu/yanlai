# M6-C Phase 2 Production Sprite Runtime Pipeline

## Objective

Establish the minimum runtime pipeline for production sprite frames.

This phase supports production idle multi-frame playback without changing gameplay, Behavior, Growth, Reveal, Save, or Desktop Foundation.

## Directory Standard

### Candidate / Validation Area

`assets/characters/cat/production/`

Used for:

- candidate frames
- motion validation
- near-final art tests
- process exports

### Runtime Sprite Area

`assets/characters/cat/sprites/<behavior>/`

Used for:

- runtime-loaded production frames
- approved or currently validated runtime frames

Runtime frame naming:

```text
frame_01.png
frame_02.png
frame_03.png
```

## Implemented

- Copied validated breathing frames into `assets/characters/cat/sprites/idle/`.
- Created runtime behavior sprite directories for idle, walk, sit, and sleep.
- CatLayer now supports multiple production frames per behavior.
- Production idle can play `frame_01.png` and `frame_02.png`.
- Validation fallback remains active when production frames are missing.
- Added `idle_fps` configuration for low-interruption idle playback speed.

## Explicitly Not Implemented

- New Behavior
- Behavior timing changes
- Growth changes
- Reveal changes
- Save changes
- Desktop Foundation changes
- Sprite sheet runtime loading
- Full animation state machine
- Production walk, sit, or sleep art completion

## Current Runtime Source

When `source=production` is enabled:

- Idle uses production frames from `assets/characters/cat/sprites/idle/`.
- Walk, sit, and sleep fall back to validation sprites until production frames are added.

When `source=validation` is enabled:

- All behaviors use validation sprites.

## Validation Status

- Project script check passes in Godot 4.7.
- Project loads in Godot 4.7.
- Production idle frames are discoverable by runtime.
- Missing production behavior frames fall back to validation assets.
- Runtime architecture remains unchanged.

## Known Limitations

- Only idle has production runtime frames at this phase.
- Runtime currently uses independent PNG frames only.
- Candidate frames must be copied or exported into `assets/characters/cat/sprites/<behavior>/` before runtime approval.

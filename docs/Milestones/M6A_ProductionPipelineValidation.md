# M6-A Phase 1 Production Companion Pipeline Validation

## Objective

Validate that the runtime can load production companion assets without changing architecture.

This milestone validates the production asset pipeline.

It does not attempt to complete the production companion.

## Implementation

### Configuration

Added asset source configuration to `config/gameplay.cfg`:

```ini
[assets]
; Asset source: "validation" or "production"
; Default is "validation" to maintain current project state.
; When "production" is selected, CatLayer attempts to load from production paths.
; Falls back to validation if production assets are unavailable.
source=validation
```

### Runtime Changes

Updated `scripts/cat/cat_layer.gd`:

- Added `PRODUCTION_SPRITE_PATHS` constant for production asset paths
- Added `ASSET_CONFIG_PATH` constant for configuration file
- Added `_asset_source` variable to track current asset source
- Added `_configure_asset_source()` function to load configuration
- Updated `_load_validation_cat_sprites()` to support both asset sources
- Added fallback logic: if production assets fail to load, falls back to validation assets

### Asset Source Selection

The selection is configuration-driven:

- Set `source=validation` in `config/gameplay.cfg` to use validation assets
- Set `source=production` in `config/gameplay.cfg` to use production assets
- Default is `validation` to avoid breaking the current project

### Fallback Behavior

If production assets are unavailable:

1. CatLayer attempts to load from production paths
2. If loading fails, falls back to validation paths
3. No runtime errors or crashes
4. Graceful degradation to current behavior

## Validation Results

- Validation assets still load correctly
- Runtime behavior unchanged
- Reveal unchanged
- Interaction unchanged
- Growth unchanged
- Save unchanged
- Switching asset source does not require code modification
- Fallback behavior works correctly

# M6-C Phase 1 Production Idle Integration

## Production Idle Assets

Created production idle sprite set:

- `assets/characters/cat/sprites/idle/1.png` — Natural resting posture
- `assets/characters/cat/sprites/idle/2.png` — Subtle breathing animation

### Design Philosophy Applied

- Calm, warm, believable house cat
- Young adult domestic cat
- Short to medium fur
- Subtle breathing animation
- Readable from one meter
- Low interruption

### Sprite Details

- Canvas size: 96x96
- Format: RGBA transparent PNG
- Frame count: 2
- Animation: Subtle breathing (body expansion)
- Style: Pixel art with intentional simplicity

## Runtime Integration

When `source=production` is set in `config/gameplay.cfg`:

- CatLayer loads from `assets/characters/cat/sprites/idle/`
- Animation cycles between frame 1 and frame 2
- Validation fallback remains available

## Validation Results

- Production idle displays correctly
- Validation fallback still works
- No runtime regression
- Behavior unchanged
- Reveal unchanged
- Growth unchanged
- Save unchanged

# M6-C Phase 2 Production Sprite Runtime Pipeline

## Runtime Directory Standard

Production candidate and runtime assets are now separated:

- Candidate / validation work: `assets/characters/cat/production/`
- Runtime-loaded sprites: `assets/characters/cat/sprites/<behavior>/`

Runtime sprite frames use:

```text
frame_01.png
frame_02.png
frame_03.png
```

## Runtime Update

- CatLayer supports multiple production frames per behavior.
- Production idle loads `frame_01.png` and `frame_02.png`.
- Missing production frames continue to fall back to validation assets.
- Idle playback speed is configured through `config/gameplay.cfg`.

## Validation Results

- Godot 4.7 script check passes.
- Project loads in Godot 4.7.
- Production idle frame loading is supported.
- Growth, Reveal, Save, Behavior, Interaction, and Desktop Foundation remain unchanged.

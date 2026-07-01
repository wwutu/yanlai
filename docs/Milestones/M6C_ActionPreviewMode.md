# M6-C Action Preview Mode

## Objective

Provide a temporary runtime preview path for candidate animation sheets.

This mode allows candidate frames under `assets/characters/cat/production/` to be played inside the real Godot desktop pet runtime before they are promoted into `assets/characters/cat/sprites/<behavior>/`.

## Implemented

- Added `config/art_preview.cfg`.
- Added CatLayer art preview loading.
- Preview frames are loaded from a configurable frame directory.
- Preview mode loops all PNG frames in sorted order.
- Current preview target:

```text
assets/characters/cat/production/cock_its_head_back/
```

## Runtime Behavior

When preview is enabled:

- CatLayer displays preview frames instead of the current behavior sprite.
- BehaviorSystem continues running unchanged.
- Growth remains unchanged.
- Reveal remains derived from Growth and still applies visually.
- Save remains unchanged.
- Interaction remains unchanged.

## Not Implemented

- No new Behavior
- No animation state machine
- No promotion into production runtime sprites
- No save data
- No gameplay logic

## How To Use

Edit:

```text
config/art_preview.cfg
```

Enable or disable preview:

```ini
[preview]
enabled=true
```

Choose candidate frame directory:

```ini
frame_dir="res://assets/characters/cat/production/cock_its_head_back"
```

Adjust preview playback speed:

```ini
fps=8.0
```

When the action is approved, copy or export the accepted frames into:

```text
assets/characters/cat/sprites/<behavior>/
```

Preview mode should be disabled before normal runtime validation.

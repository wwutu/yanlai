# M1-A Desktop Foundation

## Goal

Validate whether Godot 4.7 can run stably as the foundation for a Windows desktop pet.

## Completed

- Transparent window
- Borderless window
- Always-on-top window
- Bottom-right default placement
- Draggable window
- Single-instance runtime
- Simple circular placeholder

## Explicitly Not Implemented

- Cat
- CatBrain
- Behavior
- Animation
- Growth
- Reveal
- Draw
- Save System
- UI

## Technical Notes

- Transparent window requires project-level per-pixel transparency, window transparent background, Viewport transparent background, and Windows DisplayServer transparent flag.
- Single instance is implemented through local TCP IPC.
- `window_move_to_foreground` may be limited by Windows focus policy.

## Transparent Composition Verified

Key transparent composition pipeline:

- `get_window().transparent = true`
- `get_tree().root.transparent = true`
- Viewport transparent background
- Window transparent background
- Compatibility / OpenGL renderer

The previous black background issue came from the window itself not fully entering transparent composition.

The transparent window has now been verified through actual player-side runtime testing.

## M1-B Recommendation

- Keep the Desktop Foundation layer and cat presentation layer separated.
- The cat should exist only as window content and must not directly manage platform capabilities such as transparency, always-on-top behavior, dragging, or single-instance control.

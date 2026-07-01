# M5-A Companion Interaction Foundation

## Milestone Purpose

Establish the interaction framework for all future companion interactions.

This milestone builds a clean, independent interaction pipeline.

It is not a gameplay milestone.

## InteractionSystem

### Responsibilities

- Receive mouse interaction
- Determine whether the Validation Cat was interacted with
- Dispatch a runtime interaction event

### Ownership Boundaries

InteractionSystem owns:

- Interaction detection
- Interaction validation
- Interaction dispatch

InteractionSystem does NOT own:

- Growth
- Reveal
- Behavior
- Save
- Gameplay progression

### Event Flow

```
Mouse Click
    ↓
InteractionSystem._unhandled_input()
    ↓
_is_click_on_cat()
    ↓
interaction_detected signal
```

### Current Validation Interaction

Left mouse click on the Validation Cat.

When clicked:

- InteractionSystem emits `interaction_detected("click", position)`
- The event may be logged for validation
- Nothing else happens

### Future Extension Points

The interaction pipeline supports future extensions:

- Different interaction types (hover, double-click, right-click)
- Different target regions
- Interaction cooldowns
- Interaction queues
- Interaction chaining

## Runtime Integration

InteractionSystem is registered as a sibling node in the main scene.

It remains parallel to the existing runtime chain:

```
Desktop Time → Growth → Reveal → Render
```

InteractionSystem does not modify any system in this chain.

## Validation Result

- Project loads
- Clicking the cat reaches InteractionSystem
- Interaction event dispatch succeeds
- Growth unchanged
- Reveal unchanged
- Behavior unchanged
- Save unchanged
- Runtime chain unchanged
- Architecture boundaries remain clean

## Interaction Feel Validation

### Click Detection

Left-click on the Validation Cat reaches InteractionSystem.

The signal `interaction_detected("click", position)` is emitted.

### Hit Accuracy

Clicking on the cat triggers interaction.

Clicking clearly outside the cat does not trigger interaction.

The hit area matches the visual sprite rect.

### Right-click Compatibility

Existing right-click Growth display still works.

Left-click interaction does not break right-click behavior.

### Low Interruption

Clicking creates no popups, sounds, animations, or forced behavior changes.

InteractionSystem only emits a signal.

### System Independence

InteractionSystem does not modify:

- Growth
- Reveal
- Behavior
- Save

### Misclick Risk

The hit area is the exact sprite rect (160x130 target size).

The area feels appropriate for a pixel art cat at desktop scale.

### Feel Validation Result

- Click Detection: PASS
- Hit Accuracy: PASS
- Right-click Compatibility: PASS
- Low Interruption: PASS
- System Independence: PASS
- Misclick Risk: PASS

## Interaction Event Flow

### Signal Update

InteractionSystem now emits `interaction_requested` with:

- `type`: String (currently `"pet"`)
- `position`: Vector2 (click position)
- `target`: String (currently `"cat"`)

### BehaviorSystem Subscription

BehaviorSystem subscribes to `interaction_requested` signal.

The handler `_on_interaction_requested` receives the event.

Current behavior: log only, no behavior change.

### Event Flow

```
Mouse Click on Cat
    ↓
InteractionSystem._unhandled_input()
    ↓
_is_click_on_cat()
    ↓
interaction_requested.emit("pet", position, "cat")
    ↓
BehaviorSystem._on_interaction_requested()
    ↓
(no behavior change — validation only)
```

### Validation Result

- Project loads
- Left-click on cat emits `interaction_requested`
- BehaviorSystem receives the event
- Behavior does not change
- Growth unchanged
- Reveal unchanged
- Save unchanged
- Runtime chain unchanged
- Right-click Growth display still works

## Petting Micro Response Prototype

### Response Rules

When petted during:

- **Idle/Sit**: Brief acknowledgment with warm glow
- **Sleep**: No interruption, internal acknowledgment only
- **Walk**: No interruption, internal acknowledgment only

### Visual Response

CatLayer adds a subtle warm glow when pet is acknowledged:

- Color: `Color(1.0, 0.85, 0.6, alpha)`
- Alpha: fades in to 0.12, then fades out over 0.4 seconds
- Effect: gentle warmth, not distracting

### Behavior Response

BehaviorSystem tracks pet acknowledgment:

- `_pet_acknowledged` flag
- `_pet_acknowledge_timer` countdown
- Duration: 0.4 seconds
- No behavior transition forced
- No timing modification

### Validation Result

- Project loads
- Left-click emits pet interaction
- BehaviorSystem receives pet event
- Response is subtle
- Behavior rhythm is not broken
- Growth unchanged
- Reveal unchanged
- Save unchanged
- Right-click Growth display still works
- Low Interruption passes

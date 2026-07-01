# Interaction Design Specification v1

## 1. Interaction Philosophy

Player left-click on the cat equals petting the cat.

The cat is never treated as a desktop button.

Interaction should always feel like interacting with a living companion.

The cat is not a UI element. The cat is not a clickable object. The cat is a companion that responds to the player's presence and touch.

## 2. Companion First

Interaction exists to strengthen companionship.

Interaction is not a gameplay reward.

Interaction is not a progression mechanic.

Interaction must never interrupt normal companion rhythm.

The cat's natural behavior continues even when the player interacts. The cat remains autonomous. The player's touch is welcomed, not commanded.

## 3. Context Aware Response

Interaction responses depend on the cat's current state.

Sleeping cats should respond differently from sitting cats.

Walking cats should respond differently from resting cats.

The cat's behavior context determines how it receives and responds to interaction. A sleeping cat might stir briefly. A sitting cat might lean into the touch. A walking cat might pause and acknowledge.

Interaction responses are shaped by what the cat is already doing.

## 4. Response Priority

### Level 1: Micro Response

Small, brief acknowledgments.

Examples:

- Ear movement
- Tail movement
- Brief glance

These are the most common responses. They happen quickly and return to the previous state naturally.

### Level 2: Light Response

Slightly more noticeable reactions.

Examples:

- Small posture adjustment
- Stretch
- Yawn

These happen occasionally and feel like natural responses to being acknowledged.

### Level 3: Special Response

Occasional delightful moments.

Examples:

- Roll over
- Expose belly
- Playful reaction

These are rare and feel like the cat choosing to share a special moment with the player.

These levels are examples, not required implementations. They describe the range of possible responses.

## 5. Forbidden Directions

Interaction must never become:

- Button clicking
- Popup generator
- Reward dispenser
- Forced gameplay
- Growth shortcut
- Reveal shortcut
- Constant interruption

The cat is not a means to an end. The cat is the end.

## 6. Future Relationship

Future systems such as:

- Food
- Furniture
- Toys
- Affection
- Mood

may subscribe to Interaction events.

Interaction itself owns none of these systems.

InteractionSystem dispatches events. Other systems decide how to respond. The interaction pipeline remains clean and independent.

# M1-B Living Cat

## Goal

Validate whether a line cat can make the player feel that "the cat is alive" through behavior rhythm, readable posture differences, breathing, center-of-mass changes, and low-distraction interaction.

## Completed

- CatBrain only chooses the next behavior.
- 6 Behaviors:
  - Sit
  - LookAround
  - Sleep
  - Stretch
  - TailPlay
  - ObserveMouse
- Minimal line cat placeholder.
- Behavior rhythm configuration.
- Pose transitions.
- Subtle breathing.
- Center-of-mass changes.
- Natural pauses between behaviors.

## Explicitly Not Implemented

- Growth
- Reveal
- Draw
- Cat bed
- Furniture
- Breed
- Coat color
- UI
- Numbers
- EXP
- Audio
- Rare Event
- Final art

## Technical Notes

- Desktop Foundation and Cat Layer remain separated.
- CatBrain does not control rendering, animation, windows, or platform capabilities.
- Behaviors are independently implemented.
- Future Behavior additions should not require rewriting CatBrain.

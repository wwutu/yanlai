# PROJECT_START_HERE

## Project Name

yanlai

## Current Project Path

C:\Users\zuimi\Documents\Codex\2026-06-29\openai-developers-plugin-openai-developers-openai

## Current Milestone

Character Master v1.0 Freeze

## Current Project Stage

Character Master v1.0 Frozen

## Required Reading Order

1. PROJECT_START_HERE.md
2. docs/Design/CharacterMasterSpecification_v1.md
3. docs/Design/ProductionSpriteGuide_v1.md
4. docs/TDD/Architecture_v1.md
5. docs/Architecture/CoreArchitecture_v1.md
6. docs/TDD/RuntimeSpecification_v1.md
7. docs/Milestones/
8. docs/Changelog/CHANGELOG.md

## Completed Frozen Milestones

- M2 Architecture Freeze
- M3-A Runtime Foundation
- M3-B Behavior Foundation
- M4-A Validation Asset Pipeline
- M4-B Reveal Visual Foundation
- M5-A Companion Interaction Foundation
- M5-B Phase 2 Petting Micro Response Prototype
- Character Master v1.0

## Frozen Systems

- Architecture
- Runtime
- Behavior
- Validation Asset Pipeline
- Reveal Visual Foundation
- Companion Interaction Foundation
- Petting Micro Response Prototype

## Character Master v1.0 Freeze

Yanlai v1.0 Character Master has been frozen.

Future production artwork starts from Character Master rather than generating new concept cats. Character exploration is complete for Yanlai v1.0. Future work focuses on production assets derived from the frozen Character Master.

The Character Master Reference images are now the highest visual authority for Yanlai:

- assets/character_master/CMR_001_Resting.png
- assets/character_master/CMR_002_Calm.png
- assets/character_master/CMR_003_Sitting.png

All future Idle, Walk, Sit, Sleep, Pet, Reveal, Animation, Sprite Sheet, and Promotional artwork must inherit from these three references.

## Character Master Root States

Yanlai v1.0 CMR now has three semantic root states:

- Rest Root: `CMR_001_Resting.png`
- Relax Root: `CMR_002_Calm.png`
- Interaction Root: `CMR_003_Sitting.png`

Future production art must select the correct CMR root state before creating animation or sprite frames.

## Production Sprite Guide v1.0

Production Sprite Guide v1.0 has been established.

Future production assets follow `docs/Design/ProductionSpriteGuide_v1.md`.

The guide freezes production sprite standards, including CMR Root selection, the Sprite Consistency Rule, the One Meter Principle, and the Runtime First Rule.

## Current Interaction Capability

- Left-click = Petting
- InteractionSystem dispatches interaction events
- BehaviorSystem performs context-aware micro responses
- No new behaviors introduced
- No gameplay progression affected
- Low Interruption preserved

## Current Runtime Architecture

Desktop Time -> Growth -> Reveal -> Render

InteractionSystem remains an independent runtime service.

BehaviorSystem responds through interaction events only.

## Current Runtime Systems

- DesktopTimeSystem
- GrowthSystem
- RevealSystem
- BehaviorSystem
- InteractionSystem

## Current Behavior Foundation

- Idle
- Walk
- Sit
- Sleep

## Current Character References

### Character Master References

- assets/character_master/CMR_001_Resting.png
- assets/character_master/CMR_002_Calm.png
- assets/character_master/CMR_003_Sitting.png

### Archived Historical References

- assets/archive/concept_references/validation_cat_form_reference_v1.png
- assets/archive/concept_references/validation_cat_master_pose_v1.png

### Validation Sprites

- assets/validation/sprites/cat/idle.png
- assets/validation/sprites/cat/walk.png
- assets/validation/sprites/cat/sit.png
- assets/validation/sprites/cat/sleep.png

## Next Planned Milestone

Production assets derived from Character Master v1.0.

## Project Health

GREEN

- Architecture Stable
- Runtime Stable
- Behavior Stable
- Reveal Stable
- Interaction Stable
- Petting Prototype Stable
- Character Master v1.0 Frozen

Ready for production artwork derived from the frozen Character Master.

## Frozen Principles

- Desktop Time owns Core Growth.
- No Offline Growth.
- Growth is Continuous.
- Reveal is Derived State.
- Behavior is Runtime State.
- Save Facts, Recalculate Results.
- One-meter Principle.
- Companion First.
- Low Interruption.
- Character Master governs all future production artwork.
- Do not redesign frozen systems.

## AI Handoff Rule

Every AI tool must read PROJECT_START_HERE.md first before doing any work.


# Production Companion Art Specification v1

## 1. Purpose

This specification defines the visual standards for production companion assets.

Validation assets remain historical references only. They served their purpose during the validation phase and will not be modified or replaced.

Production assets deliver the final visual experience. They must respect the frozen architecture, behavior system, and interaction principles already established.

## 2. Character Philosophy

The companion is not a mascot.

The companion is not a toy.

The companion should feel like a living cat quietly sharing the user's workspace.

Visual priorities:

- calm
- warm
- natural
- believable
- low interruption

The cat exists beside the player, not for the player. Its presence should feel effortless and undisturbing.

## 3. Character Form

Reference the frozen Character Form Reference at `assets/references/cat/validation_cat_form_reference_v1.png`.

Future companions may differ in appearance, but body proportions and silhouette consistency should remain stable within a character. A cat should always feel like the same cat, regardless of pose or behavior.

Character Form is shared. Character Appearance is replaceable.

## 4. Animation Philosophy

Animations should be:

- subtle
- readable from one meter
- low amplitude
- slow and natural

Avoid:

- exaggerated squash and stretch
- cartoon reactions
- constant motion
- attention-seeking loops

The player should feel the cat is alive without being drawn to watch it constantly. Motion serves presence, not performance.

## 5. Companion Response Philosophy

Reference the frozen Interaction Design Specification.

Click equals Petting.

Responses should feel acknowledged, not performed.

The cat should never behave like a UI widget. A petted cat might stir, glance, or settle more deeply. It should not light up, bounce, or perform for the player.

## 6. Minimum Production Asset Set

The first production companion requires:

### Design Reference

- Character design sheet showing final appearance
- Turnaround for proportional consistency

### Color Palette

- Fur colors
- Nose and paw colors
- Eye colors
- Background transparency specification

### Behavior Sprites

| Behavior | Frames | Notes |
|----------|--------|-------|
| Idle | 2 | Default resting state |
| Sit | 2 | Calm sitting pose |
| Sleep | 2 | Resting with closed eyes |
| Walk | 4 | Smooth walking cycle |
| Pet Response | 2 | Acknowledgment, not performance |

### Reference Sheets

- Expression Reference — subtle facial variations
- Tail Reference — tail position vocabulary
- Ear Reference — ear movement vocabulary

This set represents the minimum viable production companion.

## 7. Production Companion MVP

### Required Capabilities

The first production companion should support:

- Idle
- Sit
- Walk
- Sleep
- Petting Response

These define the minimum companion experience rather than a complete behavior library. The MVP validates that production art works within the existing frozen runtime.

### Asset Groups

The minimum required asset groups:

- Character Design Reference
- Color Palette
- Expression Reference
- Ear Reference
- Tail Reference
- Sprite Assets

Frame counts and implementation details are defined separately during production.

### Design Goal

The MVP exists to validate:

- natural companionship
- visual consistency
- interaction feeling

rather than feature completeness. If the MVP feels like a living companion sharing the workspace, the foundation is correct.

### Future Expansion

Future behavior expansions may include:

- Stretch
- Look Around
- Roll Over
- Grooming
- Cursor Observation

These are future expansions and not part of the MVP. They will be added only after the MVP validates successfully.

## 8. Asset Organization Recommendation

Do not use `production` as the root asset directory. Use a character-oriented structure instead.

### Recommended Structure

```
assets/
    characters/
        cat/
            design/
                cat_design_reference_v1.png
                cat_turnaround_v1.png
            sprites/
                idle/
                    1.png
                    2.png
                sit/
                    1.png
                    2.png
                sleep/
                    1.png
                    2.png
                walk/
                    1.png
                    2.png
                    3.png
                    4.png
            responses/
                pet/
                    1.png
                    2.png
            palette/
                cat_palette_v1.png
            references/
                expressions_v1.png
                tail_v1.png
                ears_v1.png
```

### Why Character-Oriented

- Scales cleanly when adding future companions
- Keeps all character assets grouped logically
- Separates behaviors from interaction responses
- Maintains clear ownership boundaries

## 9. Naming Principles

Behavior directories must match BehaviorSystem IDs exactly.

```
sprites/
    idle/
    sit/
    walk/
    sleep/
```

Interaction responses must remain separate from behaviors.

```
responses/
    pet/
```

Do not place pet under behavior assets. Pet is an interaction response, not a behavior state.

Frame files use sequential numbering starting from 1.

Reference files use `<purpose>_v<version>.png`.

## 10. Future Expansion

Future companions reuse the same pipeline while replacing appearance only.

A new companion requires:

- New design reference
- New color palette
- New sprite sets per behavior
- New response sets per interaction

The behavior system, interaction system, and runtime architecture remain unchanged. Only the visual layer changes. This is the core benefit of the frozen architecture.

# Reveal Design Specification v1

## 1. Purpose

Reveal exists to make Growth perceptible.

Growth is invisible by nature. It accumulates through Desktop Time, but the player cannot see it directly. Reveal transforms invisible Growth into visible presence.

Reveal is not gameplay. Reveal is not progression. Reveal is visual feedback that answers the player's implicit question: "Is my cat changing?"

The cat should appear to become more complete over time, creating a gentle sense of companionship developing through shared time.

## 2. Core Principles

- Reveal is Derived State.
- Reveal owns no independent progress.
- Reveal is never saved.
- Growth remains the only source of truth.
- Companion First.
- One-meter Principle.
- Low Interruption.

## 3. Visual Direction

### Validated Direction

The current prototype uses:

- warm tint
- opacity
- soft blending

This approach was validated in M4-B Phase 1 and remains the approved visual foundation.

### Visual Goals

The cat should appear to become more complete over time.

The effect should feel:

- gentle
- natural
- continuous
- warm

The effect should be readable at normal desktop viewing distance (one meter).

### Visual Safety

The effect must avoid:

- disease-like appearance
- dirt
- broken body
- bald patches
- harsh masks
- random spots
- flashy effects

The effect must remain large-area and continuous, not patch-based.

## 4. Reveal Progression Curve

### Design Rationale

Growth accumulates linearly through Desktop Time. A linear Growth-to-Reveal mapping would make early Growth changes invisible and late Growth changes imperceptible. The progression curve shapes how Growth translates into visible Reveal.

### Curve Behavior

- Early Growth (0%–30%): Reveal changes slowly. The cat remains mostly muted. This gives the player time to notice the cat before changes become apparent.
- Middle Growth (30%–80%): Reveal becomes noticeably more apparent. The cat gains color and warmth steadily.
- Late Growth (80%–100%): Reveal gradually approaches completion. The final transition is gentle, not abrupt.

### Curve Method

The current implementation uses `smoothstep(0.0, 1.0, t)` where `t = raw_growth / 100.0`. This produces a smooth ease-in-out curve with no visible thresholds or stage switching.

### Validation Result

- No visible thresholds or stage switching.
- Transition remains smooth and continuous.
- Companion feeling remains natural.
- One-meter Principle still passes.
- Desktop readability still passes.

## 5. Validation vs Production

### Validation Reveal

Validation Reveal uses placeholder visual techniques to confirm:

- Reveal responds to Growth
- Reveal remains Derived State
- Reveal is never saved
- The visual feels safe and companion-like
- The effect is readable at desktop scale

Validation Reveal uses whole-sprite modulation, not final region-based reveal art.

### Production Reveal

Production Reveal will use final visual techniques to deliver:

- region-based reveal art
- production shaders or masks
- higher quality reveal textures
- final visual polish

Production Reveal must preserve all validated principles.

## 6. Future Expansion

Possible future improvements include:

- better masks
- production shaders
- higher quality reveal textures
- region-based reveal presentation

These are listed for awareness only. None are committed to implementation.

## 7. Out of Scope

Reveal is NOT:

- mood
- affection
- gameplay reward
- particle celebration
- achievement animation
- progression system
- save data

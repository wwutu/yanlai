# Architecture Direction

yanlai uses Modular Architecture as its primary architecture.

Systems are separated by responsibility.

Examples:

- Desktop Foundation
- DesktopTimeSystem
- CatBrain
- Behavior System
- GrowthSystem
- RevealSystem
- Cat Layer
- SaveSystem

# Architecture Freeze Summary

Architecture Freeze is recorded in `docs/Architecture/CoreArchitecture_v1.md`.

ADR references:

- `docs/Architecture/ADR/ADR-001_DesktopTimeOwnsGrowth.md`
- `docs/Architecture/ADR/ADR-002_NoOfflineGrowth.md`
- `docs/Architecture/ADR/ADR-003_GrowthIsContinuous.md`
- `docs/Architecture/ADR/ADR-004_RevealIsDerivedState.md`
- `docs/Architecture/ADR/ADR-005_SaveFactsRecalculateResults.md`
- `docs/Architecture/ADR/ADR-006_SingleWriterPrinciple.md`

Frozen architecture summary:

- Desktop Time owns Core Growth.
- There is no Offline Growth.
- Core Growth is continuous.
- Growth Efficiency may modify Core Growth, but Growth Efficiency never owns Core Growth.
- Core Growth follows the Single Writer Principle and Single Calculator Principle.
- Save Facts, Recalculate Results.
- Reveal is Derived State.
- Behavior is Runtime State.
- Persistent State, Runtime State, and Derived State remain distinct.
- Modular Architecture remains the primary architecture.

Component-based Design may be introduced later only for highly reusable capabilities, such as:

- Emotion Component
- Affection Component
- Hunger Component

The project should not migrate to a full Entity Component System at the current stage.

# System Responsibility Boundaries

## Desktop Foundation

Desktop Foundation is responsible for:

- transparent window
- borderless window
- always-on-top behavior
- dragging
- single instance

Desktop Foundation must not control:

- CatBrain
- Behavior
- Growth
- Reveal
- Cat rendering

## CatBrain

CatBrain is responsible for:

- choosing next behavior

CatBrain must not control:

- rendering
- animation details
- window management
- Growth
- Reveal
- Save

## Cat Layer

Cat Layer is responsible for:

- drawing the cat
- displaying behavior state
- displaying Derived State

Cat Layer must not decide:

- next behavior
- Core Growth
- Life Seed
- Save logic
- Desktop Foundation behavior

## DesktopTimeSystem

DesktopTimeSystem is responsible for:

- Desktop Time accumulation

DesktopTimeSystem must not control:

- Growth
- Reveal
- Save
- Behavior

## GrowthSystem

GrowthSystem is responsible for:

- Core Growth calculation
- Growth Efficiency application

GrowthSystem must not control:

- Save
- Reveal
- Behavior
- Animation
- UI
- Life Seed ownership
- Runtime persistence

## RevealSystem

RevealSystem is responsible for:

- deriving Reveal from Growth

RevealSystem must not control:

- stored Reveal state
- Core Growth modification
- Reveal persistence

## SaveSystem

SaveSystem is responsible for:

- persisting factual data

SaveSystem must not control:

- Growth calculation
- Reveal calculation
- Runtime State ownership

# Current Architecture Decision

The current architecture is intentionally simple.

Prototype systems must remain replaceable.

Do not over-engineer.

Do not introduce full component-based architecture unless future scope clearly requires it.

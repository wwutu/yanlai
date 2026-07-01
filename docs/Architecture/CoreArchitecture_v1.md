# Core Philosophy

yanlai uses Modular Architecture.

The project does not use full Component-based Architecture as its primary architecture.

The frozen architecture prioritizes:

- One-meter Principle
- Character First
- Companion Feeling
- Low Interruption
- Validation Before Production
- Freeze After Validation
- Reconstructability Principle

# Growth Architecture

Desktop Time owns Core Growth.

There is no Offline Growth.

Core Growth is continuous.

Growth Efficiency may modify Core Growth, but Growth Efficiency never owns Core Growth.

Core Growth follows the Single Writer Principle.

Core Growth follows the Single Calculator Principle.

# Runtime Architecture

Desktop Foundation, DesktopTimeSystem, CatBrain, Behavior System, GrowthSystem, RevealSystem, Cat Layer, and SaveSystem remain separated by responsibility.

Desktop Foundation owns platform-level desktop behavior.

CatBrain chooses the next behavior.

Behavior is Runtime State.

Reveal is Derived State.

Cat Layer displays behavior state and Derived State.

# State Classification

State is classified as:

- Persistent State
- Runtime State
- Derived State

# Persistent / Runtime / Derived State

Persistent State is saved.

Runtime State exists only while the application is running.

Derived State is recalculated from Persistent State and runtime context.

Behavior is Runtime State.

Reveal is Derived State.

# Save Strategy

Save Facts, Recalculate Results.

Persistent State stores facts.

Derived State is reconstructed instead of treated as authoritative saved state.

# Data Flow

DesktopTimeSystem produces Desktop Time.

GrowthSystem calculates Core Growth from Desktop Time.

Growth Efficiency modifies Core Growth without owning it.

Persistent State is loaded by SaveSystem.

Derived State is recalculated from Persistent State.

Cat Layer displays Runtime State and Derived State.

CatBrain does not control Core Growth, Reveal, Save, rendering, or window management.

# Integration Rules

Do not move Desktop Foundation responsibilities into CatBrain, Behavior System, GrowthSystem, RevealSystem, or Cat Layer.

Do not move CatBrain responsibilities into Behavior System or Cat Layer.

Do not let Behavior own Core Growth.

Do not let Reveal own Core Growth.

Do not save Derived State as authoritative state.

Do not introduce Offline Growth.

Do not introduce full Component-based Architecture as the primary architecture.

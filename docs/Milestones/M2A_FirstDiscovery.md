# M2-A First Discovery

## Goal

Validate whether a player can naturally notice "my cat is starting to show color" through a growth-driven reveal system, without UI interruption.

## Scope

This milestone validates architecture only. It is NOT the final production implementation.

## Prototype Purpose

- Prove that an immutable Life Seed can deterministically control reveal order and color.
- Prove that growth accumulation can drive visible color changes on the cat.
- Prove that a BFS-based reveal path produces natural, non-random color spread.
- Prove that player-pulled information (right-click) works without interrupting gameplay.

## Completed

- Life Seed generated on first run, saved to `user://save/life_seed.dat`.
- Growth System accumulates Core Growth, saved to `user://save/growth.dat`.
- Growth speed configurable via `config/gameplay.cfg`.
- 8 body regions with BFS-determined reveal order.
- Reveal thresholds: first region at 3%, last at 95%.
- Color overlay drawn behind line art, alpha fades in per region.
- Right-click toggles "XX%" growth display at bottom center.
- CatBrain responsibility unchanged.
- Desktop Foundation responsibility unchanged.

## Validation Results

- Transparent desktop behavior preserved.
- Six behaviors preserved.
- CatBrain still only chooses behavior.
- Newly generated cat has one Persistent State Life Seed.
- Core Growth persists across restart.
- Color reveal begins visibly at low growth.
- Reveal path does not look like random noise.
- Right-click Growth info works.
- No EXP or Level language appears.

## Known Limitations

- Placeholder colors only. Final color palette TBD.
- Growth speed is linear. Future: may curve or gate by milestones.
- Reveal regions are coarse (8 body parts). Future: finer grid or freeform masks.
- Right-click display is a toggle. Future: may add fade-out timer.
- Save format is basic Dictionary. Future: versioned format with migration.

## Explicitly Not Implemented

- Full Level 1 completion
- Cat bed
- Furniture
- Rare events
- Personality
- Stats
- Economy
- EXP
- Sound
- Steam systems
- Breed system
- Skin system
- Formal UI

## Technical Notes

- Growth/Reveal system is separate from CatBrain.
- CatBrain does not control Growth or Reveal Pattern.
- Life Seed only controls Reveal Pattern (not personality or behavior).
- Persistent State uses `user://save/` directory, not project root.

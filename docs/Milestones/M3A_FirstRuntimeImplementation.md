# M3-A Phase 2 First Runtime Implementation

## Implemented

- DesktopTimeSystem counts active desktop runtime only while the application is running.
- GrowthSystem calculates Core Growth from Desktop Time.
- Growth Efficiency exists as a multiplier with default value `1.0`.
- RevealSystem derives Reveal from Final Growth.
- SaveSystem persists factual state only.
- Existing line cat rendering continues to read Reveal as Derived State.

## Explicitly Not Implemented

- Furniture
- Mood
- Affection
- Inventory
- Economy
- Buffs beyond default Growth Efficiency
- New behavior
- New animation
- Sound
- UI polish
- Production art
- Offline Growth

## Validation Results

- Script check passed.
- Project loads in Godot 4.7.
- Desktop Time increases while running.
- Growth increases from Desktop Time.
- Reveal is derived from Growth.
- Restart restores Growth from Persistent State.
- Reveal restores by recalculation from Growth, not saved Reveal.
- No Offline Growth is added after closing and reopening.
- Save data contains only Growth, Desktop Time, and Last Exit Time.
- No Godot test process remained after validation.

## Known Limitations

- Reveal presentation remains prototype quality.
- Growth Efficiency is present only as default multiplier `1.0`.
- Existing visual presentation remains line-art placeholder.

## Runtime Integration Review

- Active GrowthSystem is `scripts/runtime/growth_system.gd`.
- Legacy compatibility wrapper `scripts/growth/growth_system.gd` was unused and removed.
- `scenes/main.tscn` references only the runtime GrowthSystem.
- CatLayer reads Growth for display only and does not calculate or write Growth.
- Reveal remains Derived State from Growth.
- SaveSystem persists only Growth, Desktop Time, and Last Exit Time.
- Desktop Time remains the only Core Growth source.
- No Offline Growth path was found in the active runtime chain.

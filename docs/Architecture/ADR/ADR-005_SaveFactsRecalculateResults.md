# ADR-005 Save Facts Recalculate Results

## Decision

Save Facts, Recalculate Results.

## Reason

Persistent State should remain stable, minimal, and reconstructable.

## Alternatives Considered

- Save every calculated result.
- Treat Derived State as authoritative saved state.

## Impact

Persistent State stores facts.

Derived State is recalculated.

Runtime State is not persisted as authoritative state.

## Status

Frozen


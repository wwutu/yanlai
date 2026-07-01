# Runtime Philosophy

Every runtime system owns only one responsibility.

No runtime system should perform another runtime system's responsibility.

Runtime systems communicate through data, not through ownership transfer.

# Core Runtime Flow

DesktopTimeSystem

v

GrowthSystem

v

RevealSystem

v

Render/UI

# Runtime Systems

## DesktopTimeSystem

### System Purpose

Own Desktop Time during active runtime.

### Responsibilities

- Count Desktop Time
- Provide accumulated runtime

### Inputs

- Runtime session activity

### Outputs

- Desktop Time
- Accumulated runtime

### Owned Data

- Desktop Time

### Forbidden Responsibilities

- Calculate Growth
- Save data
- Reveal
- Behavior

### Dependencies

- None

### Future Extension Notes

Future extensions must preserve Desktop Time ownership.

## GrowthSystem

### System Purpose

Calculate Core Growth from Desktop Time and Growth Efficiency.

### Responsibilities

- Calculate Core Growth
- Apply Growth Efficiency
- Produce Final Growth

### Inputs

- Desktop Time
- Growth Efficiency

### Outputs

- Core Growth
- Final Growth

### Owned Data

- Core Growth

### Forbidden Responsibilities

- Save
- Reveal
- Behavior
- UI
- Animation

### Dependencies

- DesktopTimeSystem

### Future Extension Notes

Future extensions may modify Growth Efficiency but must not transfer Core Growth ownership.

## RevealSystem

### System Purpose

Calculate Derived State for Reveal from Final Growth.

### Responsibilities

- Calculate Reveal Percentage
- Convert Growth into visual progress

### Inputs

- Final Growth
- Persistent State required for reconstruction

### Outputs

- Reveal Percentage
- Derived State for visual progress

### Owned Data

- None

### Forbidden Responsibilities

- Modify Growth
- Store Reveal
- Save data

### Dependencies

- GrowthSystem
- SaveSystem for Persistent State input

### Future Extension Notes

Future reveal refinement must keep Reveal as Derived State.

## SaveSystem

### System Purpose

Persist facts required for reconstruction.

### Responsibilities

Persist only:

- Growth
- Desktop Time
- Last Exit Time

### Inputs

- Persistent State facts

### Outputs

- Loaded Persistent State facts

### Owned Data

- Persistent State storage

### Forbidden Responsibilities

- Calculate Growth
- Calculate Reveal
- Own Runtime State

### Dependencies

- None

### Future Extension Notes

Future save changes must preserve Save Facts, Recalculate Results.

# Runtime Ownership Table

| Data | Owner | Readable By | Writable By |
|---|---|---|---|
| Desktop Time | DesktopTimeSystem | GrowthSystem, SaveSystem | DesktopTimeSystem |
| Growth | GrowthSystem | RevealSystem, SaveSystem | GrowthSystem |
| Reveal | RevealSystem | Render/UI | None as Persistent State |
| Last Exit Time | SaveSystem | SaveSystem | SaveSystem |
| Growth Efficiency | GrowthSystem | GrowthSystem | GrowthSystem |

# Runtime Data Flow

DesktopTimeSystem produces Desktop Time.

GrowthSystem reads Desktop Time.

GrowthSystem applies Growth Efficiency.

GrowthSystem produces Final Growth.

RevealSystem reads Final Growth.

RevealSystem calculates Derived State for visual progress.

Render/UI reads Derived State.

SaveSystem persists Persistent State facts only.

# Runtime State Classification

## Persistent State

Persistent State is saved and loaded.

Persistent State includes Growth, Desktop Time, and Last Exit Time.

## Runtime State

Runtime State exists only while the application is running.

Behavior is Runtime State.

## Derived State

Derived State is recalculated from Persistent State and runtime context.

Reveal is Derived State.

# Runtime Constraints

Reveal never owns state.

Growth owns growth only.

Desktop Time owns time only.

Save owns persistence only.

Systems communicate through data.

Systems never communicate through ownership transfer.

Core Growth follows the Single Writer Principle.

Core Growth follows the Single Calculator Principle.

Save Facts, Recalculate Results.

There is no Offline Growth.

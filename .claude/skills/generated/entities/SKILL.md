---
name: entities
description: "Skill for the Entities area of monster-strike. 14 symbols across 4 files."
---

# Entities

14 symbols | 4 files | Cohesion: 100%

## When to Use

- Working with code in `entities/`
- Understanding how Enemy, Ball, PhysicsBody work
- Modifying entities-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `entities/enemy.py` | Enemy, __init__, _calculate_weakpoint_center, update_weakpoint_center, pos (+1) |
| `core/physics_body.py` | PhysicsBody, __init__, draw |
| `core/interfaces.py` | IUpdateable, IDrawable, ICollidable |
| `entities/ball.py` | Ball, __init__ |

## Entry Points

Start here when exploring this area:

- **`Enemy`** (Class) — `entities/enemy.py:13`
- **`Ball`** (Class) — `entities/ball.py:5`
- **`PhysicsBody`** (Class) — `core/physics_body.py:5`
- **`IUpdateable`** (Class) — `core/interfaces.py:4`
- **`IDrawable`** (Class) — `core/interfaces.py:9`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `Enemy` | Class | `entities/enemy.py` | 13 |
| `Ball` | Class | `entities/ball.py` | 5 |
| `PhysicsBody` | Class | `core/physics_body.py` | 5 |
| `IUpdateable` | Class | `core/interfaces.py` | 4 |
| `IDrawable` | Class | `core/interfaces.py` | 9 |
| `ICollidable` | Class | `core/interfaces.py` | 14 |
| `update_weakpoint_center` | Method | `entities/enemy.py` | 38 |
| `pos` | Method | `entities/enemy.py` | 114 |
| `draw` | Method | `entities/enemy.py` | 66 |
| `draw` | Method | `core/physics_body.py` | 51 |
| `__init__` | Method | `entities/enemy.py` | 14 |
| `_calculate_weakpoint_center` | Method | `entities/enemy.py` | 26 |
| `__init__` | Method | `entities/ball.py` | 6 |
| `__init__` | Method | `core/physics_body.py` | 6 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Pos → _calculate_weakpoint_center` | intra_community | 3 |

## How to Explore

1. `gitnexus_context({name: "Enemy"})` — see callers and callees
2. `gitnexus_query({query: "entities"})` — find related execution flows
3. Read key files listed above for implementation details

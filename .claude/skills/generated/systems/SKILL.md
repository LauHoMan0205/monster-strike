---
name: systems
description: "Skill for the Systems area of monster-strike. 12 symbols across 7 files."
---

# Systems

12 symbols | 7 files | Cohesion: 96%

## When to Use

- Working with code in `systems/`
- Understanding how main, generate_non_overlapping_enemies, update work
- Modifying systems-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `systems/turn_manager.py` | update, _update_ball_with_substeps, _execute_enemy_turn |
| `systems/collision_manager.py` | process_ball_enemy_collisions, _calculate_damage, _add_floating_text |
| `systems/input_handler.py` | handle_events, _shoot |
| `main.py` | main |
| `utils/helpers.py` | generate_non_overlapping_enemies |
| `core/physics_world.py` | add_body |
| `core/game_context.py` | reset |

## Entry Points

Start here when exploring this area:

- **`main`** (Function) — `main.py:11`
- **`generate_non_overlapping_enemies`** (Function) — `utils/helpers.py:6`
- **`update`** (Method) — `systems/turn_manager.py:9`
- **`handle_events`** (Method) — `systems/input_handler.py:12`
- **`add_body`** (Method) — `core/physics_world.py:9`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `main` | Function | `main.py` | 11 |
| `generate_non_overlapping_enemies` | Function | `utils/helpers.py` | 6 |
| `update` | Method | `systems/turn_manager.py` | 9 |
| `handle_events` | Method | `systems/input_handler.py` | 12 |
| `add_body` | Method | `core/physics_world.py` | 9 |
| `reset` | Method | `core/game_context.py` | 22 |
| `process_ball_enemy_collisions` | Method | `systems/collision_manager.py` | 13 |
| `_update_ball_with_substeps` | Method | `systems/turn_manager.py` | 28 |
| `_execute_enemy_turn` | Method | `systems/turn_manager.py` | 37 |
| `_shoot` | Method | `systems/input_handler.py` | 39 |
| `_calculate_damage` | Method | `systems/collision_manager.py` | 39 |
| `_add_floating_text` | Method | `systems/collision_manager.py` | 45 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Main → Generate_non_overlapping_enemies` | intra_community | 3 |
| `Main → _shoot` | intra_community | 3 |
| `_update_ball_with_substeps → _execute_enemy_turn` | intra_community | 3 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Rendering | 1 calls |

## How to Explore

1. `gitnexus_context({name: "main"})` — see callers and callees
2. `gitnexus_query({query: "systems"})` — find related execution flows
3. Read key files listed above for implementation details

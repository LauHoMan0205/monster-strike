---
name: rendering
description: "Skill for the Rendering area of monster-strike. 11 symbols across 3 files."
---

# Rendering

11 symbols | 3 files | Cohesion: 87%

## When to Use

- Working with code in `rendering/`
- Understanding how get_drag_info, render, get_alive_enemies work
- Modifying rendering-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `rendering/renderer.py` | render, _draw_grid, _draw_shooter_base, _draw_enemies, _draw_ball (+2) |
| `core/game_context.py` | get_alive_enemies, are_all_enemies_dead, is_game_over |
| `systems/input_handler.py` | get_drag_info |

## Entry Points

Start here when exploring this area:

- **`get_drag_info`** (Method) — `systems/input_handler.py:53`
- **`render`** (Method) — `rendering/renderer.py:14`
- **`get_alive_enemies`** (Method) — `core/game_context.py:29`
- **`are_all_enemies_dead`** (Method) — `core/game_context.py:32`
- **`is_game_over`** (Method) — `core/game_context.py:35`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `get_drag_info` | Method | `systems/input_handler.py` | 53 |
| `render` | Method | `rendering/renderer.py` | 14 |
| `get_alive_enemies` | Method | `core/game_context.py` | 29 |
| `are_all_enemies_dead` | Method | `core/game_context.py` | 32 |
| `is_game_over` | Method | `core/game_context.py` | 35 |
| `_draw_grid` | Method | `rendering/renderer.py` | 26 |
| `_draw_shooter_base` | Method | `rendering/renderer.py` | 32 |
| `_draw_enemies` | Method | `rendering/renderer.py` | 37 |
| `_draw_ball` | Method | `rendering/renderer.py` | 41 |
| `_draw_aiming_helper` | Method | `rendering/renderer.py` | 45 |
| `_draw_ui` | Method | `rendering/renderer.py` | 64 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Is_game_over → Get_alive_enemies` | intra_community | 3 |
| `_draw_ui → Get_alive_enemies` | intra_community | 3 |
| `_draw_ui → _draw_grid` | cross_community | 3 |
| `_draw_ui → _draw_shooter_base` | cross_community | 3 |
| `_draw_ui → _draw_enemies` | cross_community | 3 |
| `_draw_ui → _draw_ball` | cross_community | 3 |
| `_draw_aiming_helper → _draw_grid` | intra_community | 3 |
| `_draw_aiming_helper → _draw_shooter_base` | intra_community | 3 |
| `_draw_aiming_helper → _draw_enemies` | intra_community | 3 |
| `_draw_aiming_helper → _draw_ball` | intra_community | 3 |

## How to Explore

1. `gitnexus_context({name: "get_drag_info"})` — see callers and callees
2. `gitnexus_query({query: "rendering"})` — find related execution flows
3. Read key files listed above for implementation details

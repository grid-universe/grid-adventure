# Action

The `Action` enum defines all available player actions.

## Actions

| Index | Action | Description |
|-------|--------|-------------|
| 0 | `UP` | Move up |
| 1 | `DOWN` | Move down |
| 2 | `LEFT` | Move left |
| 3 | `RIGHT` | Move right |
| 4 | `USE_KEY` | Unlock adjacent locked entity with matching key |
| 5 | `PICK_UP` | Collect items at current tile |
| 6 | `WAIT` | Do nothing (advance turn) |

## Use Case
Actions are primarily used with the step function of [GridAdventureEnv](grid_adventure_enviroment.md#methods).
```python
# Import
from grid_adventure.actions import Action

# Using Action enum with enviroment
obs, reward, terminated, truncated, info = env.step(Action.UP)

# Using integer index
obs, reward, terminated, truncated, info = env.step(0)  # UP
```
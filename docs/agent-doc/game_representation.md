# Game Representation

Grid Adventure operates as a turn based game. Players are supplied a snapshot of a turn of the Game. Players then return an action, which is then used to generate the snapshot.

## Types of representation
There are 3 ways for a Game Snapshot to be represented.

| Representation Type | Description |
| --- | --- |
| [GridState Representation](#gridstate-representation) | A grid based representation using 2D Array. This is the most intuitive Representation. |
| [Observation Representation](observation.md) | An RGBA Image representation using #D Array, accompanied  additional info stored in an Information Dictionary |
| [State Representation](state.md) | An Immutable world state. This is the most Comprehensive, but low level representation |

**Note**: The Capstone Project can be solved without using the **State Representation**.

&nbsp;
# GridState Representation
The GridState Representation is a grid centric representation, that is easiest for players to follow

## GridState Attributes
The GridState class has 3 categories of attributes

- Overall Configuration
- Grid Structure
- Game Status

### Overall Configuration

| Attribute | Type | Description |
|-----------|------|-------------|
| `width` | `int` | Grid width in tiles |
| `height` | `int` | Grid height in tiles |
| `movement` | `BaseMovement` | Movement function configuration |
| `objective` | `BaseObjective` | Win/lose condition configuration |
| `seed` | `int` or `None` | RNG seed for deterministic behavior |

### Grid Structure

| Attribute | Type | Description |
|-----------|------|-------------|
| `grid` | `list[list[list[BaseEntity]]]` | Grid representation where `grid[x][y]` is a list of entities at that cell |

### Game Status

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `turn` | `int` | `0` | Current turn number |
| `score` | `int` | `0` | Cumulative score |
| `win` | `bool` | `False` | True if objective met |
| `lose` | `bool` | `False` | True if losing condition met |
| `message` | `str` or `None` | `None` | Optional status message for display |
| `turn_limit` | `int` or `None` | `None` | Max turns allowed |

&nbsp;
## Available Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `GridState.add(pos, obj)` | `None` | Place entity at position `(x, y)` |
| `GridState.add_many(items)` | `None` | Place multiple entities from list of `(pos, obj)` tuples |
| `GridState.remove(pos, obj)` | `bool` | Remove specific entity by identity; returns `True` if found |
| `GridState.remove_if(pos, predicate)` | `int` | Remove entities where `predicate(obj)` is `True`; returns count |
| `GridState.move_obj(from_pos, obj, to_pos)` | `bool` | Move entity between cells; returns `True` if successful |
| `GridState.clear_cell(pos)` | `int` | Remove all entities from cell; returns count |
| `GridState.objects_at(pos)` | `list[BaseEntity]` | Return shallow copy of entities at position |
| `step(gridState, action)` | `GridState` | Generates new `GridState` with action |
| `to_state(gridState)` | `None` | Converts mutable `gridState` to immutable `State` |

Note: `pos` is of class `Position`, a (int, int)  
Note: `obj` is of class `BaseEntity`, parent class of all Entities. For more details about entities, Please refer to [Entity Classes](entities.md#entities).


# GridAdventureEnv

Grid Adventure uses an underlying game engine for the `Grid Universe` turn-based game. It implements the Gymnasium API, providing a standard interface for agents to interact with the game.

**Note**: For the purpose of the Capstone Project, knowledge of the `Grid Universe` is not required.

## Big Picture
The GridAdventureEnv holds an internal state representation ([State](state.md) class), this can be seen as the simulation. Its job is to provide player with the game representation, or "snapshot", at each turn via the `reset` or `step` function.

## Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `initial_state_fn` | `Callable[..., State]` | required | Function that generates the initial internal game state |
| `render_mode` | `str` | `"rgb_array"` | Rendering mode |
| `observation_type` | `str` | `"image"` | This determines if the game representation returned is of image ([Observation](observation.md) class) or gridstate ([GridState](game_representation.md#gridstate-representation) class)|

Note: For more details about "Observation class" & "GridState class", Please refer to [Game Representation](game_representation.md).

&nbsp;
## Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `GridAdventureEnv.reset(seed, options)` | `tuple[Observation, dict]` | Resets the internal game state and returns the game representation|
| `GridAdventureEnv.step(action)` | `tuple[Observation, float, bool, bool, dict]` | Apply one action, and returns the game representation |
| `GridAdventureEnv.render()` | `PILImage` or `None` | Render current state |
| `GridAdventureEnv.close()` | `None` | Release resources |

<!-- &nbsp;
## Basic Usage

```python
from grid_adventure.env import GridAdventureEnv
from grid_adventure.actions import Action

env = GridAdventureEnv(initial_state_fn=my_generator)
obs, info = env.reset()

done = False
while not done:
    action = Action.UP  # or your policy
    obs, reward, terminated, truncated, info = env.step(action)
    done = terminated or truncated

env.close()
``` -->

from typing import Any, Union, Callable

from grid_universe.state import State
from grid_universe.gym_env import GridUniverseEnv, Observation
from grid_universe.renderer.texture import TextureMap, DEFAULT_RESOLUTION
from grid_universe.levels.grid import Level

from grid_adventure.level import from_state
from grid_adventure.rendering import DEFAULT_ASSET_ROOT, TEXTURE_MAP


class GridAdventureEnv(GridUniverseEnv):
    """Grid Adventure environment class.

    This class extends the base `GridUniverseEnv` to incorporate
    Grid Adventure-specific configurations, entities, and objectives.
    """

    def __init__(
        self,
        initial_state_fn: Callable[..., State],
        render_mode: str = "rgb_array",
        render_resolution: int = DEFAULT_RESOLUTION,
        render_texture_map: TextureMap = TEXTURE_MAP,
        render_asset_root: str = DEFAULT_ASSET_ROOT,
        observation_type: str = "image",
        **kwargs: Any,
    ) -> None:
        super().__init__(
            initial_state_fn=initial_state_fn,
            render_mode=render_mode,
            render_resolution=render_resolution,
            render_texture_map=render_texture_map,
            render_asset_root=render_asset_root,
            observation_type=observation_type,
            **kwargs,
        )

    def _get_obs(self) -> Union[Observation, Level]:
        """
        Get the current observation from the environment. If the observation type is 'level',
        return a specialized Level view; otherwise, return the standard observation.
        """
        assert self.state is not None and self.agent_id is not None
        if self._observation_type == "level":
            return from_state(self.state)
        return super()._get_obs()

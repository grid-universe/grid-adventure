from __future__ import annotations

from typing import Callable

from grid_universe.state import State
from grid_universe.renderer.image import ImageMap

from grid_adventure.env import GridAdventureEnv
from grid_adventure.rendering import IMAGE_MAP
from grid_adventure.levels import intro as adv_intro_levels

from grid_play.config.sources.level_selection import (
    Builder,
    make_level_selection_source,
)
from grid_play.config.sources.base import register_level_source

BUILDERS: dict[str, Builder] = {
    "A0 Basic Movement": adv_intro_levels.build_level_basic_movement,
    "A1 Maze Turns": adv_intro_levels.build_level_maze_turns,
    "A2 Optional Coin Path": adv_intro_levels.build_level_optional_coin,
    "A3 One Required Gem": adv_intro_levels.build_level_required_one,
    "A4 Two Required Gems": adv_intro_levels.build_level_required_two,
    "A5 Key & Door": adv_intro_levels.build_level_key_door,
    "A6 Hazard Detour": adv_intro_levels.build_level_hazard_detour,
    "A7 Pushable Box": adv_intro_levels.build_level_pushable_box,
    "A8 Shield Powerup": adv_intro_levels.build_level_power_shield,
    "A9 Ghost Powerup": adv_intro_levels.build_level_power_ghost,
    "A10 Boots Powerup": adv_intro_levels.build_level_power_boots,
    "A11 Capstone (Simple)": adv_intro_levels.build_level_capstone_simple,
    "A12 Capstone (Advanced)": adv_intro_levels.build_level_capstone_advanced,
}


def _env_factory(
    initial_state_fn: Callable[..., State], _image_map: ImageMap
) -> GridAdventureEnv:
    sample_state: State = initial_state_fn()
    return GridAdventureEnv(
        render_mode="rgb_array",
        initial_state_fn=initial_state_fn,
        width=sample_state.width,
        height=sample_state.height,
        render_image_map=IMAGE_MAP,  # fixed art set
    )


source = make_level_selection_source(
    name="Grid Adventure Intro",
    builders=BUILDERS,
    builder_returns_level=True,  # builders return Level
    env_factory=_env_factory,
    image_maps=[IMAGE_MAP],  # single pack -> no picker
)

register_level_source(source)

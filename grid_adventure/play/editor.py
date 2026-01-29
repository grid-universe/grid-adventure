from __future__ import annotations

from collections.abc import Callable
from typing import Any

import streamlit as st

from grid_universe.state import State
from grid_universe.renderer.image import ImageMap

from grid_adventure.env import GridAdventureEnv
from grid_adventure.objectives import OBJECTIVES
from grid_adventure.movements import MOVEMENTS
from grid_adventure.rendering import IMAGE_MAP, DEFAULT_ASSET_ROOT
from grid_adventure.entities import (
    FloorEntity,
    WallEntity,
    ExitEntity,
    CoinEntity,
    GemEntity,
    KeyEntity,
    LockedDoorEntity,
    UnlockedDoorEntity,
    BoxEntity,
    LavaEntity,
    SpeedPowerUpEntity,
    ShieldPowerUpEntity,
    PhasingPowerUpEntity,
    create_agent_entity,
    create_robot_entity,
    create_moving_box_entity,
    create_portal_entity,
)

from grid_play.config.sources.base import register_level_source
from grid_play.config.sources.level_editor import ToolSpec, make_level_editor_source


# -----------------------
# Parameter UIs
# -----------------------


def agent_params() -> dict[str, Any]:
    return {
        "health": int(
            st.number_input(
                "Health", min_value=1, max_value=99, value=5, key="adv_agent_health"
            )
        )
    }


def direction_params(prefix: str) -> dict[str, Any]:
    direction = st.selectbox(
        "Direction", ["up", "down", "left", "right"], index=1, key=f"{prefix}_direction"
    )
    return {"direction": direction}


# -----------------------
# Palette
# -----------------------

PALETTE: dict[str, ToolSpec] = {
    "floor": ToolSpec(
        label="Floor",
        icon="⬜",
        factory_fn=FloorEntity,
        param_map=lambda p: {},
    ),
    "wall": ToolSpec(
        label="Wall",
        icon="🟫",
        factory_fn=WallEntity,
        param_map=lambda p: {},
    ),
    "agent": ToolSpec(
        label="Agent",
        icon="😊",
        factory_fn=create_agent_entity,
        param_map=lambda p: {"health": int(p.get("health", 5))},
        param_ui=agent_params,
    ),
    "exit": ToolSpec(
        label="Exit",
        icon="🏁",
        factory_fn=ExitEntity,
        param_map=lambda p: {},
    ),
    "coin": ToolSpec(
        label="Coin",
        icon="🪙",
        factory_fn=CoinEntity,
        param_map=lambda p: {},
    ),
    "gem": ToolSpec(
        label="Gem",
        icon="💎",
        factory_fn=GemEntity,
        param_map=lambda p: {},
    ),
    "key": ToolSpec(
        label="Key",
        icon="🔑",
        factory_fn=KeyEntity,
        param_map=lambda p: {},
    ),
    "door_locked": ToolSpec(
        label="Locked Door",
        icon="🚪",
        factory_fn=LockedDoorEntity,
        param_map=lambda p: {},
    ),
    "door_unlocked": ToolSpec(
        label="Unlocked Door",
        icon="🚪",
        factory_fn=UnlockedDoorEntity,
        param_map=lambda p: {},
    ),
    "portal": ToolSpec(
        label="Portal",
        icon="🔵",
        factory_fn=create_portal_entity,
        param_map=lambda p: {},
        description="Click two cells sequentially to pair.",
    ),
    "box": ToolSpec(
        label="Box",
        icon="📦",
        factory_fn=BoxEntity,
        param_map=lambda p: {},
    ),
    "moving_box": ToolSpec(
        label="Moving Box",
        icon="🧱",
        factory_fn=create_moving_box_entity,
        param_map=lambda p: {"direction": p.get("direction", "down")},
        param_ui=lambda: direction_params("moving_box"),
    ),
    "robot": ToolSpec(
        label="Robot",
        icon="🤖",
        factory_fn=create_robot_entity,
        param_map=lambda p: {"direction": p.get("direction", "down")},
        param_ui=lambda: direction_params("robot"),
    ),
    "lava": ToolSpec(
        label="Lava",
        icon="🔥",
        factory_fn=LavaEntity,
        param_map=lambda p: {},
    ),
    "speed": ToolSpec(
        label="Speed PowerUp",
        icon="🥾",
        factory_fn=SpeedPowerUpEntity,
        param_map=lambda p: {},
    ),
    "shield": ToolSpec(
        label="Shield PowerUp",
        icon="🛡️",
        factory_fn=ShieldPowerUpEntity,
        param_map=lambda p: {},
    ),
    "ghost": ToolSpec(
        label="Ghost PowerUp",
        icon="👻",
        factory_fn=PhasingPowerUpEntity,
        param_map=lambda p: {},
    ),
    "erase": ToolSpec(
        label="Eraser",
        icon="␡",
        factory_fn=FloorEntity,
        param_map=lambda p: {},
        description="Reset cell to floor-only.",
    ),
}


# -----------------------
# Asset root resolver (preview) + env factory
# -----------------------


def _asset_root_resolver(image_map: ImageMap) -> str:
    return DEFAULT_ASSET_ROOT


def _env_factory(
    initial_state_fn: Callable[..., State], image_map: ImageMap
) -> GridAdventureEnv:
    sample_state = initial_state_fn()
    return GridAdventureEnv(
        render_mode="rgb_array",
        initial_state_fn=initial_state_fn,
        width=sample_state.width,
        height=sample_state.height,
        render_image_map=image_map,
    )


# -----------------------
# Register LevelSource
# -----------------------

register_level_source(
    make_level_editor_source(
        name="Grid Adventure Level Editor",
        palette=PALETTE,
        image_maps=[IMAGE_MAP],
        env_factory=_env_factory,
        movement_registry=MOVEMENTS,
        objective_registry=OBJECTIVES,
        asset_root_resolver=_asset_root_resolver,
        gridstate_import_line="from grid_adventure.grid import GridState",
        movements_import_line="from grid_adventure.movements import MOVEMENTS",
        objectives_import_line="from grid_adventure.objectives import OBJECTIVES",
    )
)

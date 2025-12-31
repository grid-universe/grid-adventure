from __future__ import annotations

from typing import Any, Callable, cast

import streamlit as st

from grid_universe.state import State
from grid_universe.renderer.texture import TextureMap

from grid_play.config.sources.base import register_level_source
from grid_play.config.sources.level_editor import ToolSpec, make_level_editor_source

from grid_adventure.types import Direction
from grid_adventure.env import GridAdventureEnv
from grid_adventure.rendering import (
    TEXTURE_MAP as ADVENTURE_TEXTURE_MAP,
    DEFAULT_ASSET_ROOT,
)
from grid_adventure.objectives import objectives
from grid_adventure.moves import moves
from grid_adventure.entities import (
    AgentEntity,
    FloorEntity,
    WallEntity,
    ExitEntity,
    CoinEntity,
    GemEntity,
    KeyEntity,
    LockedDoorEntity,
    UnlockedDoorEntity,
    PortalEntity,
    BoxEntity,
    MovingBoxEntity,
    RobotEntity,
    LavaEntity,
    SpeedPowerUpEntity,
    ShieldPowerUpEntity,
    PhasingPowerUpEntity,
    create_agent_entity,
    create_robot_entity,
    create_moving_box_entity,
)


# ------------------------
# Parameter UIs (only for configurable entities with helper functions)
# ------------------------


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
    return {"direction": cast(Direction, direction)}


# ------------------------
# Builders using helper functions
# ------------------------


def build_agent(p: dict[str, Any]) -> AgentEntity:
    return create_agent_entity(health=int(p.get("health", 5)))


def build_moving_box(p: dict[str, Any]) -> MovingBoxEntity:
    return create_moving_box_entity(direction=p.get("direction", "down"))


def build_robot(p: dict[str, Any]) -> RobotEntity:
    return create_robot_entity(direction=p.get("direction", "down"))


# --- Palette specification ---

PALETTE: dict[str, ToolSpec] = {
    "floor": ToolSpec(label="Floor", icon="⬜", builder=lambda _p: FloorEntity()),
    "wall": ToolSpec(label="Wall", icon="🟫", builder=lambda _p: WallEntity()),
    "agent": ToolSpec(
        label="Agent", icon="😊", builder=build_agent, param_ui=agent_params
    ),
    "exit": ToolSpec(label="Exit", icon="🏁", builder=lambda _p: ExitEntity()),
    "coin": ToolSpec(label="Coin", icon="🪙", builder=lambda _p: CoinEntity()),
    "gem": ToolSpec(label="Gem", icon="💎", builder=lambda _p: GemEntity()),
    "key": ToolSpec(label="Key", icon="🔑", builder=lambda _p: KeyEntity()),
    "door_locked": ToolSpec(
        label="Locked Door", icon="🚪", builder=lambda _p: LockedDoorEntity()
    ),
    "door_unlocked": ToolSpec(
        label="Unlocked Door", icon="🚪", builder=lambda _p: UnlockedDoorEntity()
    ),
    "portal": ToolSpec(
        label="Portal",
        icon="🔵",
        builder=lambda _p: PortalEntity(),
        description="Click two cells sequentially to pair (auto-wired by editor).",
    ),
    "box": ToolSpec(label="Box", icon="📦", builder=lambda _p: BoxEntity()),
    "moving_box": ToolSpec(
        label="Moving Box",
        icon="🧱",
        builder=build_moving_box,
        param_ui=lambda: direction_params("moving_box"),
    ),
    "robot": ToolSpec(
        label="Robot",
        icon="🤖",
        builder=build_robot,
        param_ui=lambda: direction_params("robot"),
    ),
    "lava": ToolSpec(label="Lava", icon="🔥", builder=lambda _p: LavaEntity()),
    "speed": ToolSpec(
        label="Speed PowerUp", icon="🥾", builder=lambda _p: SpeedPowerUpEntity()
    ),
    "shield": ToolSpec(
        label="Shield PowerUp", icon="🛡️", builder=lambda _p: ShieldPowerUpEntity()
    ),
    "ghost": ToolSpec(
        label="Ghost PowerUp", icon="👻", builder=lambda _p: PhasingPowerUpEntity()
    ),
    "erase": ToolSpec(
        label="Eraser",
        icon="␡",
        builder=lambda _p: FloorEntity(),
        description="Reset cell to floor-only.",
    ),
}


# --- Environment factory for editor preview ---


def _env_factory(
    initial_state_fn: Callable[..., State], texture_map: Any
) -> GridAdventureEnv:
    sample_state = initial_state_fn()
    return GridAdventureEnv(
        render_mode="rgb_array",
        initial_state_fn=initial_state_fn,
        width=sample_state.width,
        height=sample_state.height,
        render_texture_map=texture_map,
    )


# --- Asset root resolver for preview ---


def _asset_root_resolver(texture_map: TextureMap) -> str:
    return DEFAULT_ASSET_ROOT


# --- Register LevelSource ---

register_level_source(
    make_level_editor_source(
        name="Grid Adventure Level Editor",
        palette=PALETTE,
        texture_maps=[
            ADVENTURE_TEXTURE_MAP
        ],  # single map -> picker hidden; ensures correct art set
        env_factory=_env_factory,
        move_fn_registry=moves,
        objective_fn_registry=objectives,
        asset_root_resolver=_asset_root_resolver,
    )
)

from typing import Callable
import numpy as np
from grid_adventure.env import GridAdventureEnv
from grid_adventure.levels import intro
from grid_universe.levels.convert import level_fn_to_initial_state_fn
from grid_universe.actions import Action
from grid_universe.renderer.texture import TextureMap


def test_env_image_observation_with_temp_assets(
    make_temp_assets: Callable[[dict[str, str]], str],
):
    # Build a minimal asset set: map known appearances in intro levels to image stems
    # Use a subset that appears in basic_movement (human, floor, wall, exit)
    stems = {"human": "human", "floor": "floor", "wall": "wall", "exit": "exit"}
    asset_root = make_temp_assets(stems)

    env = GridAdventureEnv(
        initial_state_fn=level_fn_to_initial_state_fn(intro.build_level_basic_movement),
        observation_type="image",
        seed=100,
        render_asset_root=asset_root,
        render_texture_map=TextureMap(
            {
                ("human", tuple([])): "human.png",
                ("floor", tuple([])): "floor.png",
                ("wall", tuple([])): "wall.png",
                ("exit", tuple([])): "exit.png",
            }
        ),
        render_resolution=128,
    )
    obs, _ = env.reset()
    assert "image" in obs and "info" in obs
    img = obs["image"]
    assert isinstance(img, np.ndarray)
    assert img.ndim == 3 and img.shape[2] == 4  # RGBA
    # Step and confirm image still valid
    obs2, reward, terminated, truncated, info2 = env.step(Action.WAIT)
    assert obs2["image"].shape == obs["image"].shape
    env.close()

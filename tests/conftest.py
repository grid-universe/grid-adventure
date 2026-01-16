from pathlib import Path
import pytest
from typing import Iterator, Callable
from PIL import Image

from grid_universe.levels.convert import to_state, level_fn_to_initial_state_fn
from grid_universe.levels.grid import Level
from grid_universe.state import State
from grid_adventure.levels import intro
from grid_adventure.env import GridAdventureEnv


@pytest.fixture(scope="session")
def small_level() -> Level:
    # Use the simplest level to keep tests fast/stable
    return intro.build_level_basic_movement(seed=100)


@pytest.fixture(scope="session")
def small_state(small_level: Level) -> State:
    return to_state(small_level)


@pytest.fixture
def level_env() -> Iterator[GridAdventureEnv]:
    # observation_type="level" avoids any real rendering/assets
    env = GridAdventureEnv(
        initial_state_fn=level_fn_to_initial_state_fn(intro.build_level_basic_movement),
        observation_type="level",
        width=7,
        height=5,
    )
    yield env
    env.close()


@pytest.fixture
def make_temp_assets(tmp_path: Path) -> Callable[[dict[str, str]], str]:
    """
    Create a minimal asset directory structure for a subset of IMAGE_MAP entries.
    Pass a dict mapping logical name -> filename stem; generates tiny RGBA PNGs.
    Returns the asset root path.
    """

    def _create(asset_names: dict[str, str]) -> str:
        root = tmp_path / "assets"
        root.mkdir(parents=True, exist_ok=True)

        # Create per-appearance dirs or files matching Grid Adventure IMAGE_MAP
        # We generate 16x16 opaque squares for simplicity.
        for stem in set(asset_names.values()):
            # Image file
            img = Image.new("RGBA", (16, 16), (200, 200, 200, 255))
            file_path = root / f"{stem}.png"
            img.save(file_path)

        return str(root)

    return _create

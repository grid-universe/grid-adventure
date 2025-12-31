from grid_adventure.env import GridAdventureEnv
from grid_adventure.levels import intro
from grid_universe.levels.grid import Level
from grid_universe.levels.convert import level_fn_to_initial_state_fn


def test_env_returns_level_observation():
    env = GridAdventureEnv(
        initial_state_fn=level_fn_to_initial_state_fn(intro.build_level_capstone),
        observation_type="level",
    )
    obs, _ = env.reset()
    assert isinstance(obs, Level)
    # Step with a valid action (e.g., WAIT)
    from grid_universe.actions import Action

    obs2, reward, terminated, truncated, info2 = env.step(Action.WAIT)
    assert isinstance(obs2, Level)
    assert isinstance(reward, float)
    assert terminated in (True, False)
    assert truncated in (True, False)
    assert isinstance(info2, dict)
    env.close()

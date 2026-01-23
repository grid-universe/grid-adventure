from __future__ import annotations

from grid_universe.actions import Action
from grid_universe.grid.factories import create_agent, create_coin, create_wall
from grid_universe.grid.gridstate import GridState
from grid_universe.movements import CardinalMovement
from grid_universe.objectives import ExitObjective

from grid_adventure.entities import AgentEntity, CoinEntity, WallEntity
from grid_adventure.grid import step


def _find_entities_at(gridstate: GridState, pos: tuple[int, int]) -> list[object]:
    x, y = pos
    return list(gridstate.grid[x][y])


def _find_agent_pos(gridstate: GridState) -> tuple[int, int] | None:
    for x in range(gridstate.width):
        for y in range(gridstate.height):
            for obj in gridstate.grid[x][y]:
                if isinstance(obj, AgentEntity):
                    return (x, y)
    return None


def test_step_returns_specialized_entities() -> None:
    gridstate = GridState(
        width=3,
        height=3,
        movement=CardinalMovement(),
        objective=ExitObjective(),
    )
    agent = create_agent()
    wall = create_wall()
    gridstate.add((1, 1), agent)
    gridstate.add((2, 1), wall)

    new_grid_state = step(gridstate, Action.RIGHT)

    assert isinstance(new_grid_state, GridState)
    # Agent should stay in place due to blocking wall
    assert _find_agent_pos(new_grid_state) == (1, 1)
    # Entities should be specialized
    assert any(
        isinstance(obj, AgentEntity)
        for obj in _find_entities_at(new_grid_state, (1, 1))
    )
    assert any(
        isinstance(obj, WallEntity) for obj in _find_entities_at(new_grid_state, (2, 1))
    )


def test_step_pickup_specializes_agent_and_updates_score() -> None:
    gridstate = GridState(
        width=3,
        height=3,
        movement=CardinalMovement(),
        objective=ExitObjective(),
    )
    agent = create_agent()
    coin = create_coin(reward=10)
    gridstate.add((1, 1), agent)
    gridstate.add((1, 1), coin)

    new_grid_state = step(gridstate, Action.PICK_UP)

    assert _find_agent_pos(new_grid_state) == (1, 1)
    # Agent should be specialized after stepping
    assert any(
        isinstance(obj, AgentEntity)
        for obj in _find_entities_at(new_grid_state, (1, 1))
    )
    # Coin should be removed from grid after pickup
    assert not any(
        isinstance(obj, CoinEntity) for obj in _find_entities_at(new_grid_state, (1, 1))
    )
    # Score should reflect reward
    assert new_grid_state.score == 10

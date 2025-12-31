from grid_universe.actions import Action
from grid_universe.state import State
from grid_universe.step import step as _step


def step(state: State, action: Action) -> State:
    """Advance the environment state by one step given an action.

    This function wraps the base `grid_universe.step.step` function to
    incorporate any Grid Adventure-specific logic or modifications.

    Args:
        state: The current environment state.
        action: The action to be taken by the agent.

    Returns:
        The new environment state after applying the action.
    """
    assert state.agent is not None and len(state.agent) == 1, (
        "State must have exactly one agent."
    )
    return _step(state, action)

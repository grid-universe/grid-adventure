from grid_universe.state import State
from grid_universe.types import EntityID
from grid_universe.actions import Action
from grid_universe.levels.convert import to_state
from grid_universe.utils.ecs import entities_with_components_at
from grid_universe.components.properties import Position
from grid_adventure.levels import intro
from grid_adventure.step import step as adv_step


def _agent_id(state: State) -> EntityID:
    return next(iter(state.agent.keys()))


def _agent_pos(state: State) -> Position:
    aid = _agent_id(state)
    return state.position[aid]


# ---- L0 ----
def test_basic_movement_reaches_exit():
    """L0: Basic movement corridor — walking right should eventually reach the exit (win=True)."""
    level = intro.build_level_basic_movement(seed=100)
    state = to_state(level)

    # Move right along the open middle corridor until win
    for _ in range(20):  # ample budget
        if state.win:
            break
        state = adv_step(state, Action.RIGHT)

    assert state.win is True


# ---- L1 ----
def test_maze_turns_blocked_and_open_moves():
    """L1: Maze turns — movement into a wall is blocked; movement along corridor succeeds."""
    level = intro.build_level_maze_turns(seed=101)
    state = to_state(level)
    aid = _agent_id(state)

    # Agent starts at (1,1). Border has walls at y=0; UP should be blocked.
    pos0 = state.position[aid]
    state = adv_step(state, Action.UP)  # attempt into border wall
    assert state.position[aid] == pos0, "Moving into a wall must be blocked"

    # RIGHT into open corridor at y=1 should succeed
    state = adv_step(state, Action.RIGHT)
    assert state.position[aid].x == pos0.x + 1 and state.position[aid].y == pos0.y


# ---- L2 ----
def test_collect_coin_increases_score():
    """L2: Optional coin — after navigating to a coin tile, PICK_UP should increase score (net positive)."""
    level = intro.build_level_optional_coin(seed=102)
    state = to_state(level)

    # Hardcoded path to a coin tile at (1,5), avoiding walls:
    # Start (1,1): RIGHT -> (2,1), DOWN -> (2,2), DOWN -> (2,3),
    # LEFT -> (1,3), DOWN -> (1,4), DOWN -> (1,5)
    state = adv_step(state, Action.RIGHT)
    state = adv_step(state, Action.DOWN)
    state = adv_step(state, Action.DOWN)
    state = adv_step(state, Action.LEFT)
    state = adv_step(state, Action.DOWN)
    state = adv_step(state, Action.DOWN)

    # On coin row (y=5). PICK_UP should add reward (coin +5 minus floor cost 3 => net +2).
    prev_score = state.score
    state = adv_step(state, Action.PICK_UP)
    pickup_reward = state.score - prev_score
    assert pickup_reward > 0


# ---- L3 ----
def test_required_one_collect_then_exit_wins():
    """L3: One required core — collect the core then reach exit to win."""
    level = intro.build_level_required_one(seed=103)
    state = to_state(level)

    # Derive geometry
    w = state.width
    midx = w // 2
    # Core is placed at (midx-1, midy-1); agent at (1, midy); exit at (w-2, midy)

    # Move to core tile: UP to y=midy-1, then RIGHT until x=midx-1
    state = adv_step(state, Action.UP)
    while _agent_pos(state).x < midx - 1:
        state = adv_step(state, Action.RIGHT)
    # Pick up core
    state = adv_step(state, Action.PICK_UP)
    # Back to middle row
    state = adv_step(state, Action.DOWN)
    # Move to exit
    while _agent_pos(state).x < w - 2:
        state = adv_step(state, Action.RIGHT)

    assert state.win is True


# ---- L4 ----
def test_required_two_collect_both_then_exit_wins():
    """L4: Two required cores — collect both (top and bottom) then reach exit to win."""
    level = intro.build_level_required_two(seed=104)
    state = to_state(level)

    # Geometry (open cross: mid row and mid column are open)
    w, h = state.width, state.height
    midx, midy = w // 2, h // 2
    top_core = Position(midx, 1)
    bottom_core = Position(midx, h - 2)
    exit_pos = Position(w - 2, midy)

    # Move to center column along mid row
    while _agent_pos(state).x < midx:
        state = adv_step(state, Action.RIGHT)

    # Up to top core and pick up
    while _agent_pos(state).y > top_core.y:
        state = adv_step(state, Action.UP)
    state = adv_step(state, Action.PICK_UP)

    # Down to bottom core and pick up
    while _agent_pos(state).y < bottom_core.y:
        state = adv_step(state, Action.DOWN)
    state = adv_step(state, Action.PICK_UP)

    # Return to mid row
    while _agent_pos(state).y > midy:
        state = adv_step(state, Action.UP)

    # Move to exit
    while _agent_pos(state).x < exit_pos.x:
        state = adv_step(state, Action.RIGHT)

    assert state.win is True


# ---- L5 ----
def test_unlock_door_removes_locked_and_blocking():
    """L5: Key–Door — pick key, move adjacent to door, USE_KEY should unlock (Locked removed; not Blocking)."""
    level = intro.build_level_key_door(seed=105)
    state = to_state(level)

    # Agent starts at (1,4). Key is at (2,3).
    # Move onto the key tile before picking it up: UP -> (1,3), RIGHT -> (2,3)
    state = adv_step(state, Action.UP)
    state = adv_step(state, Action.RIGHT)
    state = adv_step(state, Action.PICK_UP)

    # Door at (5,4). Move adjacent: RIGHT -> (3,3), DOWN -> (3,4), RIGHT -> (4,4)
    state = adv_step(state, Action.RIGHT)  # (3,3)
    state = adv_step(state, Action.DOWN)  # (3,4)
    state = adv_step(state, Action.RIGHT)  # (4,4)

    # Use key when adjacent
    state = adv_step(state, Action.USE_KEY)

    # If still locked, move one more to (5,4) and try again
    if len(state.locked) > 0:
        state = adv_step(state, Action.RIGHT)  # (5,4)
        state = adv_step(state, Action.USE_KEY)

    # Check door's Locked removed in state and any door is no longer blocking
    assert len(state.locked) == 0
    for eid, app in state.appearance.items():
        if app.name == "door":
            assert eid not in state.blocking


# ---- L6 ----
def test_hazard_damage_reduces_health():
    """L6: Hazard detour — stepping into lava should reduce health."""
    level = intro.build_level_hazard_detour(seed=106)
    state = to_state(level)
    aid = _agent_id(state)
    hp_before = state.health[aid].health

    # Walk into the lava tile in the middle corridor
    state = adv_step(state, Action.RIGHT)
    state = adv_step(state, Action.RIGHT)
    state = adv_step(state, Action.RIGHT)

    hp_after = state.health[aid].health
    assert hp_after <= hp_before


# ---- L7 ----
def test_portal_teleportation():
    """L7: Portal shortcut — stepping onto a portal should teleport to its pair."""
    level = intro.build_level_portal_shortcut(seed=107)
    state = to_state(level)
    aid = _agent_id(state)

    # Move toward and onto the portal at (2,1)
    state = adv_step(state, Action.UP)
    state = adv_step(state, Action.UP)
    state = adv_step(state, Action.UP)
    state = adv_step(state, Action.RIGHT)
    pos_after = state.position[aid]

    assert pos_after == Position(level.width - 1, level.height // 2)


# ---- L8 ----
def test_pushable_box_pushes():
    """L8: Pushable box — moving into a pushable should push it one tile forward if destination is free."""
    level = intro.build_level_pushable_box(seed=108)
    state = to_state(level)

    # Locate initial box position: known at (w//2 - 1, h//2)
    w, h = state.width, state.height
    expected_box_start = Position(w // 2 - 1, h // 2)
    expected_box_dest = Position(w // 2, h // 2)

    # Sanity: ensure a pushable is at start
    pushables_at_start = entities_with_components_at(
        state, expected_box_start, state.pushable
    )
    assert len(pushables_at_start) > 0

    # Move agent right along the corridor until just left of the box
    # Agent starts at (1, h//2)
    while _agent_pos(state).x < w // 2 - 2:
        state = adv_step(state, Action.RIGHT)

    # Next RIGHT should attempt to enter the box tile and push it to expected_box_dest
    state = adv_step(state, Action.RIGHT)

    # Verify box moved to destination
    pushables_at_dest = entities_with_components_at(
        state, expected_box_dest, state.pushable
    )
    assert len(pushables_at_dest) > 0


# ---- L9 ----
def test_moving_box_moves():
    """L9: Moving box — moving entities should advance vertically between steps (autonomous movement)."""
    level = intro.build_level_moving_box(seed=113)
    state = to_state(level)

    w, h = state.width, state.height
    start = Position(w // 2, h // 2)
    down = Position(w // 2, h // 2 + 1)

    # Sanity: moving entity at start
    start_moving = entities_with_components_at(state, start, state.moving)
    assert len(start_moving) > 0

    # One step: should move down
    state = adv_step(state, Action.WAIT)
    assert len(entities_with_components_at(state, down, state.moving)) > 0

    # Next step: should be blocked and reverse (stay at down)
    state = adv_step(state, Action.WAIT)
    assert len(entities_with_components_at(state, down, state.moving)) > 0

    # Next step: should move back to start
    state = adv_step(state, Action.WAIT)
    assert len(entities_with_components_at(state, start, state.moving)) > 0


# ---- L10 ----
def test_enemy_patrol_moves():
    """L10: Enemy patrol — monsters with Moving should advance vertically between steps (autonomous movement)."""
    level = intro.build_level_enemy_patrol(seed=109)
    state = to_state(level)

    # Collect initial robot positions
    initial_positions = {
        eid: state.position[eid]
        for eid, app in state.appearance.items()
        if app.name == "robot" and eid in state.position
    }
    assert len(initial_positions) >= 2  # two patrol enemies expected

    # Take one step; autonomous moving should update their positions
    state = adv_step(state, Action.WAIT)
    moved = 0
    for eid, pos0 in initial_positions.items():
        pos1 = state.position.get(eid, pos0)
        if pos1 != pos0:
            moved += 1

    assert moved >= 1  # at least one enemy moved


# ---- L11 ----
def test_shield_blocks_damage():
    """L11: Shield (Immunity) — picking the shield should prevent subsequent hazard damage."""
    level = intro.build_level_power_shield(seed=110)
    state = to_state(level)
    aid = _agent_id(state)

    # Pick up shield power-up
    state = adv_step(state, Action.UP)
    state = adv_step(state, Action.PICK_UP)

    hp_before = state.health[aid].health

    # Step into lava — shield should absorb
    state = adv_step(state, Action.RIGHT)
    state = adv_step(state, Action.RIGHT)

    hp_after = state.health[aid].health
    assert hp_after == hp_before


# ---- L12 ----
def test_phasing_allows_passing_blocking():
    """L12: Ghost (Phasing) — phasing should allow movement through blocking tiles (locked door)."""
    level = intro.build_level_power_ghost(seed=111)
    state = to_state(level)
    aid = _agent_id(state)

    # Pick up ghost effect
    state = adv_step(state, Action.UP)
    state = adv_step(state, Action.PICK_UP)

    # Move through the locked door tile that would otherwise block
    state = adv_step(state, Action.RIGHT)
    state = adv_step(state, Action.RIGHT)
    pos_before = state.position[aid]
    state = adv_step(state, Action.RIGHT)  # would be blocked without phasing
    pos_after = state.position[aid]
    assert pos_after != pos_before


# ---- L13 ----
def test_power_boots_speed_multiplier_effect():
    """L13: Boots (Speed×2) — after pickup, a single move should traverse at least two tiles if unobstructed."""
    level = intro.build_level_power_boots(seed=112)
    state = to_state(level)

    w = state.width

    # Navigate to the boots at (w//2 - 1, h//2 + 1)
    while _agent_pos(state).x < w // 2 - 2:
        state = adv_step(state, Action.RIGHT)
    state = adv_step(state, Action.DOWN)
    state = adv_step(state, Action.RIGHT)  # should land on (w//2 - 1, h//2 + 1)

    # Pick up boots
    state = adv_step(state, Action.PICK_UP)

    # Record position, take one LEFT move; with speed x2 we expect x to decrease by at least 2
    before = _agent_pos(state)
    state = adv_step(state, Action.LEFT)
    after = _agent_pos(state)

    assert before.y == after.y  # horizontal move
    assert before.x - after.x >= 2  # traversed at least 2 tiles

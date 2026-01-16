from grid_universe.levels.grid import Level
from grid_adventure.moves import cardinal_move_fn
from grid_adventure.objectives import collect_and_exit_objective_fn, exit_objective_fn
from grid_adventure.entities import (
    create_agent_entity,
    FloorEntity,
    WallEntity,
    ExitEntity,
    CoinEntity,
    GemEntity,
    KeyEntity,
    LockedDoorEntity,
    LavaEntity,
    BoxEntity,
    SpeedPowerUpEntity,
    ShieldPowerUpEntity,
    PhasingPowerUpEntity,
)


TURN_LIMIT = 50


def _floors(level: Level) -> None:
    for y in range(level.height):
        for x in range(level.width):
            level.add((x, y), FloorEntity())


def _border(level: Level) -> None:
    for x in range(level.width):
        level.add((x, 0), WallEntity())
        level.add((x, level.height - 1), WallEntity())
    for y in range(level.height):
        level.add((0, y), WallEntity())
        level.add((level.width - 1, y), WallEntity())


def build_level_basic_movement(seed: int = 100) -> Level:
    w, h = 7, 5
    level = Level(
        w,
        h,
        move_fn=cardinal_move_fn,
        objective_fn=exit_objective_fn,
        seed=seed,
        turn_limit=TURN_LIMIT,
    )
    _floors(level)
    level.add((1, h // 2), create_agent_entity())
    level.add((w - 2, h // 2), ExitEntity())
    for y in range(h):
        if y != h // 2:
            level.add((w // 2, y), WallEntity())
    return level


def build_level_maze_turns(seed: int = 101) -> Level:
    w, h = 9, 7
    level = Level(
        w,
        h,
        move_fn=cardinal_move_fn,
        objective_fn=exit_objective_fn,
        seed=seed,
        turn_limit=TURN_LIMIT,
    )
    _floors(level)
    _border(level)
    for x in range(2, w - 2):
        level.add((x, 2), WallEntity())
    for x in range(2, w - 2):
        if x != w // 2:
            level.add((x, h - 3), WallEntity())
    level.add((1, 1), create_agent_entity())
    level.add((w - 2, h - 2), ExitEntity())
    return level


def build_level_optional_coin(seed: int = 102) -> Level:
    w, h = 9, 7
    level = Level(
        w,
        h,
        move_fn=cardinal_move_fn,
        objective_fn=exit_objective_fn,
        seed=seed,
        turn_limit=TURN_LIMIT,
    )
    _floors(level)
    _border(level)
    level.add((1, 2), WallEntity())
    level.add((3, 3), WallEntity())
    for x in range(3, w - 2):
        level.add((x, 2), WallEntity())
    for x in range(2, w - 2):
        if x != w // 2:
            level.add((x, h - 3), WallEntity())
    level.add((1, 1), create_agent_entity())
    level.add((w - 2, h - 2), ExitEntity())
    for x in range(1, w - 2, 1):
        level.add((x, h - 2), CoinEntity())
    return level


def build_level_required_one(seed: int = 103) -> Level:
    w, h = 9, 7
    level = Level(
        w,
        h,
        move_fn=cardinal_move_fn,
        objective_fn=collect_and_exit_objective_fn,
        seed=seed,
        turn_limit=TURN_LIMIT,
    )
    _floors(level)
    _border(level)
    for y in range(1, h - 1):
        if y != h // 2:
            level.add((w // 2, y), WallEntity())
    level.add((1, h // 2), create_agent_entity())
    level.add((w - 2, h // 2), ExitEntity())
    level.add((w // 2 - 1, h // 2 - 1), GemEntity())
    return level


def build_level_required_two(seed: int = 104) -> Level:
    w, h = 11, 9
    level = Level(
        w,
        h,
        move_fn=cardinal_move_fn,
        objective_fn=collect_and_exit_objective_fn,
        seed=seed,
        turn_limit=TURN_LIMIT,
    )
    _floors(level)
    _border(level)
    midx, midy = w // 2, h // 2
    for x in range(1, w - 1):
        for y in range(1, h - 1):
            if x != midx and y != midy:
                level.add((x, y), WallEntity())
    level.add((1, midy), create_agent_entity())
    level.add((w - 2, midy), ExitEntity())
    level.add((midx, 1), GemEntity())
    level.add((midx, h - 2), GemEntity())
    return level


def build_level_key_door(seed: int = 105) -> Level:
    w, h = 11, 9
    level = Level(
        w,
        h,
        move_fn=cardinal_move_fn,
        objective_fn=exit_objective_fn,
        seed=seed,
        turn_limit=TURN_LIMIT,
    )
    _floors(level)
    for y in range(h):
        if y != h // 2:
            level.add((w // 2, y), WallEntity())
    level.add((1, h // 2), create_agent_entity())
    level.add((w - 2, h // 2), ExitEntity())
    level.add((2, h // 2 - 1), KeyEntity())
    level.add((w // 2, h // 2), LockedDoorEntity())
    return level


def build_level_hazard_detour(seed: int = 106) -> Level:
    w, h = 11, 9
    level = Level(
        w,
        h,
        move_fn=cardinal_move_fn,
        objective_fn=exit_objective_fn,
        seed=seed,
        turn_limit=TURN_LIMIT,
    )
    _floors(level)
    level.add((1, h // 2), create_agent_entity(health=3))
    level.add((w - 2, h // 2), ExitEntity())
    level.add((w // 2 - 1, h // 2), LavaEntity())
    level.add((w - 3, h // 2), LavaEntity())

    for y in range(1, h - 1):
        if y != h // 2:
            level.add((w // 2 - 1, y), WallEntity())
    for y in range(2, h - 2):
        if y != h // 2:
            level.add((w - 3, y), WallEntity())
    
    return level


def build_level_pushable_box(seed: int = 108) -> Level:
    w, h = 11, 9
    level = Level(
        w,
        h,
        move_fn=cardinal_move_fn,
        objective_fn=exit_objective_fn,
        seed=seed,
        turn_limit=TURN_LIMIT,
    )
    _floors(level)
    for y in range(h):
        if y != h // 2:
            level.add((w // 2, y), WallEntity())
    level.add((1, h // 2), create_agent_entity())
    level.add((w - 2, h // 2), ExitEntity())
    level.add((w // 2 - 1, h // 2), BoxEntity())
    return level


def build_level_power_shield(seed: int = 110) -> Level:
    w, h = 11, 9
    level = Level(
        w,
        h,
        move_fn=cardinal_move_fn,
        objective_fn=exit_objective_fn,
        seed=seed,
        turn_limit=TURN_LIMIT,
    )
    _floors(level)
    level.add((1, h // 2), create_agent_entity(2))
    level.add((w - 2, h // 2), ExitEntity())
    for y in range(h):
        if y != h // 2:
            level.add((w // 2, y), WallEntity())
    level.add((2, h // 2 - 3), ShieldPowerUpEntity())
    level.add((w // 2, h // 2), LavaEntity())
    return level


def build_level_power_ghost(seed: int = 111) -> Level:
    w, h = 13, 9
    level = Level(
        w,
        h,
        move_fn=cardinal_move_fn,
        objective_fn=exit_objective_fn,
        seed=seed,
        turn_limit=TURN_LIMIT,
    )
    _floors(level)
    level.add((1, h // 2), create_agent_entity())
    level.add((w - 2, h // 2), ExitEntity())
    for y in range(h):
        level.add((w // 2, y), WallEntity())
    level.add((2, h // 2 - 3), PhasingPowerUpEntity())
    return level


def build_level_power_boots(seed: int = 112) -> Level:
    w, h = 13, 9
    level = Level(
        w,
        h,
        move_fn=cardinal_move_fn,
        objective_fn=exit_objective_fn,
        seed=seed,
        turn_limit=TURN_LIMIT,
    )
    _floors(level)
    level.add((1, h // 2), create_agent_entity(1))
    level.add((w - 2, h // 2), ExitEntity())
    for y in range(h):
        if y not in [h // 2, h // 2 + 1]:
            level.add((w // 2, y), WallEntity())
            level.add((w // 2 + 1, y), WallEntity())
            level.add((w // 2 + 2, y), WallEntity())
    level.add((w // 2 - 1, h // 2 + 1), SpeedPowerUpEntity())
    return level


def build_level_capstone_simple(seed: int = 113) -> Level:
    level = Level(
        width=7,
        height=7,
        move_fn=cardinal_move_fn,
        objective_fn=exit_objective_fn,
        seed=seed,
        turn_limit=TURN_LIMIT,
    )

    _floors(level)

    # Agent
    level.add((0, 0), create_agent_entity())

    # Walls (grouped and added in one pass)
    wall_coords = [
        # Row 0
        (3, 0),
        (5, 0),
        # Row 1
        (1, 1),
        # Row 2
        (1, 2),
        (3, 2),
        (4, 2),
        (6, 2),
        # Row 3
        (0, 3),
        (3, 3),
        (5, 3),
        # Row 4
        (1, 4),
        # Row 5
        (3, 5),
        (5, 5),
        (6, 5),
        # Row 6
        (1, 6),
        (3, 6),
    ]
    level.add_many([(pos, WallEntity()) for pos in wall_coords])

    # Items and doors
    level.add((6, 3), GemEntity())
    level.add((0, 4), KeyEntity())
    level.add((3, 4), LockedDoorEntity())

    # Exit
    level.add((6, 6), ExitEntity())

    return level

def build_level_capstone_advanced(seed: int = 113) -> Level:
    level = Level(
        width=7,
        height=7,
        move_fn=cardinal_move_fn,
        objective_fn=collect_and_exit_objective_fn,
        seed=seed,
        turn_limit=TURN_LIMIT,
    )
    _floors(level)

    # Agent and Exit
    level.add((0, 0), create_agent_entity(health=1))
    level.add((0, 6), ExitEntity())

    # Walls
    wall_pos = [
        (3, 0),
        (0, 1), (1, 1), (3, 1), (5, 1),
        (3, 2), (5, 2),
        (1, 3),
        (1, 4), (3, 4), (5, 4),
        (1, 5), (2, 5), (3, 5), (5, 5),
    ]
    for p in wall_pos:
        level.add(p, WallEntity())

    # Pushable box
    level.add((2, 1), BoxEntity())

    # Gems
    level.add((0, 5), GemEntity())
    level.add((6, 3), GemEntity())

    # Coins
    coin_pos = [
        (1, 2), (4, 2),
        (3, 3),
        (6, 5),
        (2, 6), (3, 6)
    ]
    for p in coin_pos:
        level.add(p, CoinEntity())

    # Powerups
    level.add((0, 2), SpeedPowerUpEntity())
    level.add((2, 3), PhasingPowerUpEntity())
    level.add((4, 0), ShieldPowerUpEntity())

    # Key-door pair
    level.add((4, 4), KeyEntity())
    level.add((1, 6), LockedDoorEntity())

    # Hazards
    level.add((5, 3), LavaEntity())

    return level

from grid_universe.grid.gridstate import GridState
from grid_universe.grid.convert import to_state
from grid_universe.grid.factories import (
    create_agent,
    create_floor,
    create_wall,
    create_exit,
    create_coin,
    create_core,
    create_key,
    create_door,
    create_portal,
    create_box,
    create_monster,
    create_hazard,
    create_speed_effect,
    create_immunity_effect,
    create_phasing_effect,
)
from grid_universe.components.properties.appearance import Appearance
from grid_universe.grid.entity import Entity
from grid_universe.movements import BaseMovement
from grid_universe.objectives import BaseObjective

from grid_adventure.grid import specialize_entities, from_state
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
)


def _flatten(gridstate: GridState):
    for x, col in enumerate(gridstate.grid):
        for y, cell in enumerate(col):
            for obj in cell:
                yield (x, y, obj)


def test_specialize_every_entity_type():
    """Ensure each generic Entity type is specialized to the correct subclass and placed at the right coordinates."""
    # Sandbox gridstate with one of each kind
    gridstate = GridState(
        width=10,
        height=10,
        movement=BaseMovement(
            name="test", description="Test", function=lambda s, e, a: []
        ),
        objective=BaseObjective(
            name="test", description="Test", functions=(lambda s, e: False,)
        ),
        seed=123,
    )

    coords = {
        "agent": (0, 0),
        "floor": (1, 0),
        "wall": (2, 0),
        "exit": (3, 0),
        "coin": (4, 0),
        "core": (5, 0),
        "key": (6, 0),
        "locked_door": (7, 0),
        "unlocked_door": (8, 0),
        "portal_a": (0, 1),
        "portal_b": (1, 1),
        "box": (2, 1),
        "moving_box": (3, 1),
        "monster": (4, 1),
        "lava": (5, 1),
        "speed": (6, 1),
        "shield": (7, 1),
        "phasing": (8, 1),
    }

    # Populate
    gridstate.add(coords["agent"], create_agent())
    gridstate.add(coords["floor"], create_floor())
    gridstate.add(coords["wall"], create_wall())
    gridstate.add(coords["exit"], create_exit())
    gridstate.add(coords["coin"], create_coin())
    gridstate.add(coords["core"], create_core(required=True))
    gridstate.add(coords["key"], create_key(key_id="A"))
    gridstate.add(coords["locked_door"], create_door(key_id="A"))
    # Unlocked door: appearance only, no Locked
    gridstate.add(
        coords["unlocked_door"], Entity(appearance=Appearance(name="door", priority=6))
    )
    # Portals
    p1 = create_portal()
    p2 = create_portal(pair=p1)
    gridstate.add(coords["portal_a"], p1)
    gridstate.add(coords["portal_b"], p2)
    # Boxes
    gridstate.add(coords["box"], create_box(pushable=True))
    gridstate.add(
        coords["moving_box"],
        create_box(
            pushable=False,
            moving_direction="right",
            moving_on_collision="bounce",
            moving_speed=1,
        ),
    )
    # Hostiles / hazards
    gridstate.add(coords["monster"], create_monster(damage=1, lethal=False))
    gridstate.add(coords["lava"], create_hazard("lava", damage=2, lethal=True))
    # Power-ups
    gridstate.add(coords["speed"], create_speed_effect(multiplier=2, time=5))
    gridstate.add(coords["shield"], create_immunity_effect(usage=5))
    gridstate.add(coords["phasing"], create_phasing_effect(time=5))

    specialized = specialize_entities(gridstate)

    # Build a quick index: (x,y) -> list of specialized types at that cell
    by_pos: dict[tuple[int, int], list[type]] = {}
    for x, y, obj in _flatten(specialized):
        by_pos.setdefault((x, y), []).append(type(obj))

    # Helper to assert there is exactly one instance of expected class at coordinate
    def assert_at(pos: tuple[int, int], cls: type):
        types_here = by_pos.get(pos, [])
        count = sum(1 for t in types_here if issubclass(t, cls))
        assert count == 1, (
            f"Expected exactly one {cls.__name__} at {pos}, found {count} among {types_here}"
        )

    # Coordinate checks (each at the expected cell)
    assert_at(coords["agent"], AgentEntity)
    assert_at(coords["floor"], FloorEntity)
    assert_at(coords["wall"], WallEntity)
    assert_at(coords["exit"], ExitEntity)
    assert_at(coords["coin"], CoinEntity)
    assert_at(coords["core"], GemEntity)
    assert_at(coords["key"], KeyEntity)
    assert_at(coords["locked_door"], LockedDoorEntity)
    assert_at(coords["unlocked_door"], UnlockedDoorEntity)
    # Two portals, one each at the two coordinates (pairing is wired after conversion; here we only check type/placement)
    assert_at(coords["portal_a"], PortalEntity)
    assert_at(coords["portal_b"], PortalEntity)
    assert_at(coords["box"], BoxEntity)
    assert_at(coords["moving_box"], MovingBoxEntity)
    assert_at(coords["monster"], RobotEntity)
    assert_at(coords["lava"], LavaEntity)
    assert_at(coords["speed"], SpeedPowerUpEntity)
    assert_at(coords["shield"], ShieldPowerUpEntity)
    assert_at(coords["phasing"], PhasingPowerUpEntity)

    # Presence counts (aggregate)
    counts = {
        "AgentEntity": 0,
        "FloorEntity": 0,
        "WallEntity": 0,
        "ExitEntity": 0,
        "CoinEntity": 0,
        "GemEntity": 0,
        "KeyEntity": 0,
        "LockedDoorEntity": 0,
        "UnlockedDoorEntity": 0,
        "PortalEntity": 0,
        "BoxEntity": 0,
        "MovingBoxEntity": 0,
        "RobotEntity": 0,
        "LavaEntity": 0,
        "SpeedPowerUpEntity": 0,
        "ShieldPowerUpEntity": 0,
        "PhasingPowerUpEntity": 0,
    }
    for _, _, obj in _flatten(specialized):
        name = type(obj).__name__
        if name in counts:
            counts[name] += 1

    # Exactly one of each, except portals (2)
    assert counts["AgentEntity"] == 1
    assert counts["FloorEntity"] == 1
    assert counts["WallEntity"] == 1
    assert counts["ExitEntity"] == 1
    assert counts["CoinEntity"] == 1
    assert counts["GemEntity"] == 1
    assert counts["KeyEntity"] == 1
    assert counts["LockedDoorEntity"] == 1
    assert counts["UnlockedDoorEntity"] == 1
    assert counts["PortalEntity"] == 2
    assert counts["BoxEntity"] == 1
    assert counts["MovingBoxEntity"] == 1
    assert counts["RobotEntity"] == 1
    assert counts["LavaEntity"] == 1
    assert counts["SpeedPowerUpEntity"] == 1
    assert counts["ShieldPowerUpEntity"] == 1
    assert counts["PhasingPowerUpEntity"] == 1

    # Behavioral/attribute checks (portal pairing is established during GridState->State conversion; not asserted here)
    # MovingBox must have Moving; Box must not
    moving_box = next(
        obj for _, _, obj in _flatten(specialized) if isinstance(obj, MovingBoxEntity)
    )
    box = next(obj for _, _, obj in _flatten(specialized) if isinstance(obj, BoxEntity))
    assert getattr(moving_box, "moving") is not None
    assert getattr(box, "moving", None) is None

    # Monster/Lava have damage components
    monster = next(
        obj for _, _, obj in _flatten(specialized) if isinstance(obj, RobotEntity)
    )
    lava = next(
        obj for _, _, obj in _flatten(specialized) if isinstance(obj, LavaEntity)
    )
    assert getattr(monster, "damage") is not None
    assert getattr(lava, "damage") is not None

    # Power-ups carry correct effect components
    speed = next(
        obj
        for _, _, obj in _flatten(specialized)
        if isinstance(obj, SpeedPowerUpEntity)
    )
    shield = next(
        obj
        for _, _, obj in _flatten(specialized)
        if isinstance(obj, ShieldPowerUpEntity)
    )
    phasing = next(
        obj
        for _, _, obj in _flatten(specialized)
        if isinstance(obj, PhasingPowerUpEntity)
    )
    assert getattr(speed, "speed") is not None
    assert getattr(shield, "immunity") is not None
    assert getattr(phasing, "phasing") is not None

    # Door semantics
    locked_door = next(
        obj for _, _, obj in _flatten(specialized) if isinstance(obj, LockedDoorEntity)
    )
    unlocked_door = next(
        obj
        for _, _, obj in _flatten(specialized)
        if isinstance(obj, UnlockedDoorEntity)
    )
    assert getattr(locked_door, "locked") is not None
    assert getattr(unlocked_door, "locked", None) is None

    # Coin vs Gem semantics
    coin = next(
        obj for _, _, obj in _flatten(specialized) if isinstance(obj, CoinEntity)
    )
    gem = next(obj for _, _, obj in _flatten(specialized) if isinstance(obj, GemEntity))
    assert getattr(coin, "rewardable") is not None
    assert getattr(gem, "requirable") is not None


def test_specialize_roundtrip_preserves_types_and_coordinates():
    """Round‑trip through State -> Grid Adventure GridState should preserve specialization and coordinates."""
    # Reuse a comprehensive sandbox
    gridstate = GridState(
        width=10,
        height=10,
        movement=BaseMovement(
            name="test", description="Test", function=lambda s, e, a: []
        ),
        objective=BaseObjective(
            name="test", description="Test", functions=(lambda s, e: False,)
        ),
        seed=456,
    )

    coords = {
        "agent": (0, 0),
        "floor": (1, 0),
        "wall": (2, 0),
        "exit": (3, 0),
        "coin": (4, 0),
        "core": (5, 0),
        "key": (6, 0),
        "locked_door": (7, 0),
        "unlocked_door": (8, 0),
        "portal_a": (0, 1),
        "portal_b": (1, 1),
        "box": (2, 1),
        "moving_box": (3, 1),
        "monster": (4, 1),
        "lava": (5, 1),
        "speed": (6, 1),
        "shield": (7, 1),
        "phasing": (8, 1),
    }

    # Populate objects
    gridstate.add(coords["agent"], create_agent())
    gridstate.add(coords["floor"], create_floor())
    gridstate.add(coords["wall"], create_wall())
    gridstate.add(coords["exit"], create_exit())
    gridstate.add(coords["coin"], create_coin())
    gridstate.add(coords["core"], create_core(required=True))
    gridstate.add(coords["key"], create_key(key_id="A"))
    gridstate.add(coords["locked_door"], create_door(key_id="A"))
    gridstate.add(
        coords["unlocked_door"], Entity(appearance=Appearance(name="door", priority=6))
    )
    p1 = create_portal()
    p2 = create_portal(pair=p1)
    gridstate.add(coords["portal_a"], p1)
    gridstate.add(coords["portal_b"], p2)

    gridstate.add(coords["box"], create_box(pushable=True))
    gridstate.add(
        coords["moving_box"],
        create_box(
            pushable=False,
            moving_direction="right",
            moving_on_collision="bounce",
            moving_speed=1,
        ),
    )
    gridstate.add(coords["monster"], create_monster(damage=1, lethal=False))
    gridstate.add(coords["lava"], create_hazard("lava", damage=2, lethal=True))
    gridstate.add(coords["speed"], create_speed_effect(multiplier=2, time=5))
    gridstate.add(coords["shield"], create_immunity_effect(usage=5))
    gridstate.add(coords["phasing"], create_phasing_effect(time=5))

    # Specialize -> State -> specialized GridState roundtrip
    specialized = specialize_entities(gridstate)
    state = to_state(specialized)
    roundtrip_level = from_state(state)

    # Helper for lookups by coord
    def types_at(pos: tuple[int, int]) -> set[str]:
        x, y = pos
        return {type(obj).__name__ for obj in roundtrip_level.grid[x][y]}

    # Expected types per coordinate after roundtrip
    expected = {
        coords["agent"]: {"AgentEntity"},
        coords["floor"]: {"FloorEntity"},
        coords["wall"]: {"WallEntity"},
        coords["exit"]: {"ExitEntity"},
        coords["coin"]: {"CoinEntity"},
        coords["core"]: {"GemEntity"},
        coords["key"]: {"KeyEntity"},
        coords["locked_door"]: {"LockedDoorEntity"},
        coords["unlocked_door"]: {"UnlockedDoorEntity"},
        coords["portal_a"]: {"PortalEntity"},
        coords["portal_b"]: {"PortalEntity"},
        coords["box"]: {"BoxEntity"},
        coords["moving_box"]: {"MovingBoxEntity"},
        coords["monster"]: {"RobotEntity"},
        coords["lava"]: {"LavaEntity"},
        coords["speed"]: {"SpeedPowerUpEntity"},
        coords["shield"]: {"ShieldPowerUpEntity"},
        coords["phasing"]: {"PhasingPowerUpEntity"},
    }

    for pos, want in expected.items():
        have = types_at(pos)
        assert want.issubset(have), f"At {pos}, expected {want}, found {have}"

    # Portal pairing should be established after roundtrip
    portals: list[PortalEntity] = []
    for _, row in enumerate(roundtrip_level.grid):
        for _, cell in enumerate(row):
            portals.extend([obj for obj in cell if isinstance(obj, PortalEntity)])
    assert len(portals) == 2
    assert hasattr(portals[0], "portal_pair_ref")
    assert hasattr(portals[1], "portal_pair_ref")
    assert portals[0].portal_pair_ref is portals[1]
    assert portals[1].portal_pair_ref is portals[0]

    # MovingBox remains moving; Box remains non-moving
    moving_box = next(
        obj
        for row in roundtrip_level.grid
        for cell in row
        for obj in cell
        if isinstance(obj, MovingBoxEntity)
    )
    box = next(
        obj
        for row in roundtrip_level.grid
        for cell in row
        for obj in cell
        if isinstance(obj, BoxEntity)
    )
    assert getattr(moving_box, "moving") is not None
    assert getattr(box, "moving", None) is None

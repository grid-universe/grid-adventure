from pyrsistent import pset
from dataclasses import dataclass

from grid_universe.components.effects.immunity import Immunity
from grid_universe.components.effects.phasing import Phasing
from grid_universe.components.effects.speed import Speed
from grid_universe.components.effects.time_limit import TimeLimit
from grid_universe.components.effects.usage_limit import UsageLimit
from grid_universe.components.properties.agent import Agent
from grid_universe.components.properties.appearance import Appearance
from grid_universe.components.properties.blocking import Blocking
from grid_universe.components.properties.collectible import Collectible
from grid_universe.components.properties.collidable import Collidable
from grid_universe.components.properties.cost import Cost
from grid_universe.components.properties.damage import Damage
from grid_universe.components.properties.exit import Exit
from grid_universe.components.properties.health import Health
from grid_universe.components.properties.inventory import Inventory
from grid_universe.components.properties.key import Key
from grid_universe.components.properties.locked import Locked
from grid_universe.components.properties.pushable import Pushable
from grid_universe.components.properties.requirable import Requirable
from grid_universe.components.properties.rewardable import Rewardable
from grid_universe.components.properties.status import Status
from grid_universe.levels.entity import BaseEntity

from grid_adventure.constants import (
    DEFAULT_AGENT_HEALTH,
    COIN_REWARD,
    HAZARD_DAMAGE,
    FLOOR_COST,
    KEY_DOOR_ID,
    PHASING_POWERUP_DURATION,
    SHIELD_POWERUP_USAGE,
    SPEED_POWERUP_DURATION,
    SPEED_POWERUP_MULTIPLIER,
)


# Base entity classes with common components.


@dataclass(repr=False)
class CollidableEntity(BaseEntity):
    collidable: Collidable = Collidable()


@dataclass(repr=False)
class BlockingEntity(BaseEntity):
    blocking: Blocking = Blocking()


@dataclass(repr=False)
class PushableEntity(BaseEntity):
    pushable: Pushable = Pushable()


@dataclass(repr=False)
class CollectibleEntity(BaseEntity):
    collectible: Collectible = Collectible()


# Entity definitions.


@dataclass(repr=False)
class AgentEntity(CollidableEntity):
    agent: Agent = Agent()
    appearance: Appearance = Appearance(name="human", priority=0)
    health: Health = Health(
        health=DEFAULT_AGENT_HEALTH, max_health=DEFAULT_AGENT_HEALTH
    )
    inventory: Inventory = Inventory(pset())
    status: Status = Status(pset())

    def set_health(self, health: int) -> None:
        """Set the health of the agent."""
        assert self.health is not None, (
            "AgentEntity must have a Health component to set health."
        )
        self.health = Health(health=health, max_health=health)


@dataclass(repr=False)
class FloorEntity(BaseEntity):
    appearance: Appearance = Appearance(name="floor", background=True, priority=10)
    cost: Cost = Cost(amount=FLOOR_COST)


@dataclass(repr=False)
class WallEntity(BlockingEntity):
    appearance: Appearance = Appearance(name="wall", background=True, priority=9)


@dataclass(repr=False)
class ExitEntity(BaseEntity):
    appearance: Appearance = Appearance(name="exit", priority=9)
    exit: Exit = Exit()


@dataclass(repr=False)
class CoinEntity(CollectibleEntity):
    appearance: Appearance = Appearance(name="coin", icon=True, priority=4)
    rewardable: Rewardable = Rewardable(amount=COIN_REWARD)


@dataclass(repr=False)
class GemEntity(CollectibleEntity):
    appearance: Appearance = Appearance(name="gem", icon=True, priority=4)
    requirable: Requirable = Requirable()


@dataclass(repr=False)
class KeyEntity(CollectibleEntity):
    appearance: Appearance = Appearance(name="key", icon=True, priority=4)
    key: Key = Key(key_id=KEY_DOOR_ID)


@dataclass(repr=False)
class LockedDoorEntity(BlockingEntity):
    appearance: Appearance = Appearance(name="door", priority=6)
    locked: Locked = Locked(key_id=KEY_DOOR_ID)


@dataclass(repr=False)
class UnlockedDoorEntity(BaseEntity):
    appearance: Appearance = Appearance(name="door", priority=6)


@dataclass(repr=False)
class BoxEntity(BlockingEntity, PushableEntity):
    appearance: Appearance = Appearance(name="box", priority=2)


@dataclass(repr=False)
class LavaEntity(CollidableEntity):
    appearance: Appearance = Appearance(name="lava", priority=7)
    damage: Damage = Damage(amount=HAZARD_DAMAGE)


@dataclass(repr=False)
class SpeedPowerUpEntity(CollectibleEntity):
    appearance: Appearance = Appearance(name="boots", icon=True, priority=4)
    speed: Speed = Speed(multiplier=SPEED_POWERUP_MULTIPLIER)
    time_limit: TimeLimit = TimeLimit(amount=SPEED_POWERUP_DURATION)


@dataclass(repr=False)
class ShieldPowerUpEntity(CollectibleEntity):
    appearance: Appearance = Appearance(name="shield", icon=True, priority=4)
    immunity: Immunity = Immunity()
    usage_limit: UsageLimit = UsageLimit(amount=SHIELD_POWERUP_USAGE)


@dataclass(repr=False)
class PhasingPowerUpEntity(CollectibleEntity):
    appearance: Appearance = Appearance(name="ghost", icon=True, priority=4)
    phasing: Phasing = Phasing()
    time_limit: TimeLimit = TimeLimit(amount=PHASING_POWERUP_DURATION)


# Helper functions to create entities with specific configurations.


def create_agent_entity(health: int = DEFAULT_AGENT_HEALTH) -> AgentEntity:
    """Helper to create an agent entity with specified health."""
    agent = AgentEntity()
    agent.set_health(health)
    return agent

# State Representation
The state representation is the same internal representation used by the Grid Adventure game, stores information in various attributes, tracked by EntityID of each Entity. It is the most comprehensive of the 3 representations, and the used to generate the GridState and Observation representations. 

## WARNING ON STATE SPACE
The Capstone Project can be solved without using the **State Representation**, however the State Representation is included for a lower level acess to the representation.

## State Attributes
The state Class represents the Game snapshot with the following 4 types of attributes.

- Level Configuration
- Effect Configuration
- Property Componenets
- Game Status

### Level Configuration

| Attribute | Type | Description |
|-----------|------|-------------|
| `width` | `int` | Grid width in tiles |
| `height` | `int` | Grid height in tiles |
| `movement` | `BaseMovement` | Movement functions allowed |
| `objective` | `BaseObjective` | Objective of the level |

### Effect Components

All effect stores are `PMap[EntityID, Component]`.  
Note: `PMap` is an Immutable Dictionary, dictionary methods are available.

| Attribute | Mapped Component | Description |
|-----------|-----------|-------------|
| `immunity` | `Immunity` | Damage immunity effects |
| `phasing` | `Phasing` | Pass-through-walls effects |
| `speed` | `Speed` | Movement multiplier effects |
| `time_limit` | `TimeLimit` | Effect duration (remaining steps) |
| `usage_limit` | `UsageLimit` | Effect uses (remaining count) |

### Property Components

All property stores are `PMap[EntityID, Component]`.  
Note: `PMap` is an Immutable Dictionary, dictionary methods are available.

| Attribute | Mapped Component | Description |
|-----------|-----------|-------------|
| `agent` | [`Agent`](entities.md#agententity) | Player-controlled entities |
| `appearance` | `Appearance` | Visual rendering properties |
| `blocking` | [`Blocking`](entities.md#blockingentity) | Obstacles that block movement |
| `collectible` | [`Collectible`](entities.md#collectibleentity) | Items that can be picked up |
| `collidable` | [`Collidable`](entities.md#collidable-entities) | Entities triggering collision events |
| `cost` | `Cost` | Entities that inflict movement cost |
| `damage` | [`Damage`](entities.md#lava-entity) | Entities that deal damage on contact |
| `dead` | `Dead` | Dead/incapacitated entities |
| `exit` | [`Exit`](entities.md#exitentity) | Level exit points |
| `health` | `Health` | Entity health (current/max) |
| `inventory` | `Inventory` | Items held by entities |
| `key` | [`Key`](entities.md#keyentity) | Keys that unlock `Locked` entities |
| `locked` | [`Locked`](entities.md#lockeddoorentity) | Locked doors/entities |
| `position` | `Position` | Entity grid positions |
| `pushable` | [`Pushable`](entities.md#pushableentity) | Entities that can be pushed |
| `requirable` | [`Requirable`](entities.md#gementity) | Must-collect items for objectives |
| `rewardable` | [`Rewardable`](entities.md#coinentity) | Entities granting score rewards |
| `status` | `Status` | Active status effects on entities |

### Game Status

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `turn` | `int` | `0` | Current turn number |
| `score` | `int` | `0` | Cumulative score |
| `win` | `bool` | `False` | True if objective met |
| `lose` | `bool` | `False` | True if losing condition met |
| `message` | `str` or `None` | `None` | Optional status message for display |
| `turn_limit` | `int` or `None` | `None` | Max turns allowed |
| `seed` | `int` or `None` | `None` | RNG seed for deterministic behavior |

&nbsp;
## Usage Example
All effects and components are represented by Entities in the Grid Adventure game. Each entity is assigned a unique EntityID at creation. This EntityID is used to map to each attribute of the Entity. For more details about entities, Please refer to [Entity Classes](entities.md#entities).

---                                                                                                                                                                               
Example 1: Player Entity
                                                                
A player entity with EntityID = 1 that has position, health, appearance, and agent components:  
    
&emsp;&emsp;state.position[1]   = Position(x=3, y=5)  
&emsp;&emsp;state.health[1]     = Health(health=100, max_health=100)  
&emsp;&emsp;state.appearance[1] = Appearance(name="human", priority=10)  
&emsp;&emsp;state.agent[1]      = Agent()  
&emsp;&emsp;state.inventory[1]  = Inventory(item_ids=pset([2, 3]))  # holds items 2 and 3   

The same EntityID appears in multiple component stores, each holding a different aspect of that entity.

---
Example 2: Status Effect Entity

An immunity effect with EntityID = 50 applied to the player (EntityID = 1):

&emsp;&emsp;state.immunity[50]   = Immunity()  
&emsp;&emsp;state.time_limit[50] = TimeLimit(amount=10)  # lasts 10 turns  
&emsp;&emsp;state.status[1]      = Status(effect_ids=pset([50]))  # player has effect 50  

The effect itself is an entity (EntityID = 50) stored in immunity and time_limit. The player's status component references this effect by its ID.

---

## Useful Methods

| Method | Description |
|--------|-------------|
| `state.description` | Property returning `PMap` of all non-empty state attributes |
| `from_state(state)` | Converts immutable `State` to mutable `GridState` |
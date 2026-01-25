# Entities

## Warning on Entities.
The Entities in Grid Adventure has been created so as to make them consistent. All entities, with the exception of `AgentEntity`, of the same class will be uniform. That is to say their underlying attributes are constant, and there is no need to check them for the purposes of the Capstone Project. 

&nbsp;
## Entity Types
There are in general 5 types of Entities

|Entity Types|Description|
|---|---|
| CollidableEntity | Recognisable for possession of `collidable` attribute of `Collidable` class|
| BlockingEntity | Recognisable for possession of `blocking` attribute of `Blocking` class|
| PushableEntity | Recognisable for possession of `pushable` attribute of `Pushable` class|
| CollectibleEntity | Recognisable for possession of `collectible` attribute of `Colelctible` class|
| Others | All other entities|

&nbsp;
# Collidable Entities
This are entities which can pass through each other but will trigger interactions when this happens. These entities are recognisable for possession of `collidable` attribute of `Collidable` class.  

There are in total 2 relevant Collidable Entities.

- AgentEntity 
- LavaEntity  

&nbsp;
## AgentEntity
This is the entity controlled by the user.

|Attribute|Type|Description|
|---|---|---|
|health|Health Class|Health to give the agent, constitutes Max and current health|
|inventory|Inventory Class|List of Entity that represents the Agents inventory|
|status|Status Class|List of Entity that represebts the Status Active on Agent|

|Available Methods|Inputs|Description|
|---|---|---|
|set_health|health: int|Sets agent health|

&nbsp;
## Lava Entity
This is a damaging entity that the agent can walk through

Note: Lava has a fixed Damage

&nbsp;

# BlockingEntity
This are entities which cannot be passed through by Collidable Entities. These entities are recognisable for possession of `blocking` attribute of `Blocking` class.  

There are in total 3 relevant BlockingEntity. 

- WallEntity
- LockedDoorEntity 
- BoxEntity  

Note that the Box is also a PushableEntity.  

&nbsp;
## WallEntity
This is a wall entity that the agent cannot walk through nor push. The wall entity has no atributes.

&nbsp;
## BoxEntity
This is a movable blocking entity, that the agent can push but not walk through. The box entity has no attributes.

Note: that the box is also a Pushable Entity

&nbsp;
## LockedDoorEntity
This is a blocking entity that the agent cannot through nor push. This entity becomes a [UnlockedDoorEntity](#unlockeddoorentity), when a [KeyEntity](#keyentity) is used on it

|Attribute|Type|Description|
|---|---|---|
|locked|Locked Class|Locked class that saves the key_id matching that of KeyEntity|

Note: Each level can only have up to 1 key - door pair. For each door, it is gauranteed a key exists and vice-versa.

&nbsp;

# PushableEntity
This are entities which are pushable by the Agent. These entities are recognisable for possession of `pushable` attribute of `Pushable` class. 

There is only 1 relevant PushableEntity, it is the BoxEntity. For documentation of box, see the [BoxEntity](#boxentity).

&nbsp;

# CollectibleEntity
This are entities which are collectable by the Agent. These entities are recognisable for possession of `collectible` attribute of `Collectible` class. 

There are in total 6 relevant CollectibleEntity.

- CoinEntity
- GemEntity
- KeyEntity
- SpeedPowerUpEntity
- ShieldPowerUpEntity
- PhasingPowerUpEntity  

&nbsp;
## CoinEntity
This is an **optional** collectible that provides a score when collected by the agent. 

|Attribute|Type|Description|
|---|---|---|
|rewardable|Rewardable Class|The score provided for picking up the coin|

Note: Score received for collecting a coin is fixed at 5.

&nbsp;
## GemEntity
This is a **compulsary** Collectible to be collected by agent before it can enter the exit. The GemEntity has no attributes.


&nbsp;
## KeyEntity
This is a Collectible required to unlock a [LockedDoorEntity](#lockeddoorentity)

|Attribute|Type|Description|
|---|---|---|
|key|Key Class|Key class that saves key_id matching that of LockedDoorEntity|

Note: Each level can only have up to 1 key - door pair. For each door, it is gauranteed a key exists and vice-versa.

&nbsp;
## SpeedPowerUpEntity
This is a collectible granting agent the ability to walk a multiple of tiles in 1 turn for a duration of time.

|Attribute|Type|Description|
|---|---|---|
|speed|Speed Class|Speed class that saves multiplier, indicating speed up provided|
|time_limit|TimeLimit Class|TimeLimit class that saves amount, indicating number of turns powerup is active|

Note: Speed multiplier is a constant at 2.
Note: Time limit is a constant at 5 steps.

&nbsp;
## ShieldPowerUpEntity
This is a collectible granting agent immunity while walking on damaging tiles for a duration of time.

|Attribute|Type|Description|
|---|---|---|
|time_limit|TimeLimit Class|TimeLimit class that saves amount, indicating number of turns powerup is active|

Note: Time limit is a constant at 5 steps.

&nbsp;
## PhasingPowerUpEntity
This is a collectible granting agent ability to walk through [BlockingEntity](#blockingentity) for a duration of time.

|Attribute|Type|Description|
|---|---|---|
|time_limit|TimeLimit Class|TimeLimit class that saves amount, indicating number of turns powerup is active|

Note: Time limit is a constant at 5 steps.

&nbsp;
#Other Entities
These Entities extend directly from BaseEntity. They are either non interactable entities which are purely for aesthetic purposes, or in the case of ExitEntity & FloorEntity, entities with special purposes.

&nbsp;
## ExitEntity
This are unique Exit Entity and serve as the exit objective. The ExitEntity has no other attribtues.

&nbsp;
## FloorEntity 
Floor entities are not interactable with agent. They also serve the unique purpose of introducing cost for walking over tiles.

|Attribute|Type|Description|
|---|---|---|
|cost|Cost Class|Cost of walking across the floor|

Note: Cost for each floor tile is a constant at 3.

&nbsp;
##UnlockedDoorEntity 
UnlockedDoorEntity are not interactable with agent, serving only aesthetic purpose. They are the unlocked version of the [LockedDoorEntity](#lockeddoorentity). The UnlockedDoorEntity has no attributes.
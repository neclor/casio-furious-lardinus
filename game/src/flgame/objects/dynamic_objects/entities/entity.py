from gamekit.math.vectors.vector2 import Vector2
from gamekit.math.utils import clampf

from flgame.context import GameContext
from flgame.objects.dynamic_objects.dynamic_object import DynamicObject


class Entity(DynamicObject):
    __slots__ = ("speed", "max_health", "health", "dead")

    speed: int
    max_health: int
    health: int
    dead: bool


    def __init__(self, context: GameContext, position: Vector2) -> None:
        super().__init__(context, position)
        self.collidable = True
        self.speed = 64
        self.max_health = 100
        self.health = 100
        self.dead = False


    def take_damage(self, damage: int) -> None:
        if damage <= 0:
            return
        self.health = int(clampf(self.health - damage, 0, self.max_health))
        if self.health == 0:
            self.die()


    def take_heal(self, heal: int) -> None:
        if heal <= 0:
            return
        self.health = int(clampf(self.health + heal, 0, self.max_health))


    def die(self) -> None:
        self.dead = True
        self.context.world.remove(self)

from gamekit.math.vectors.vector2 import Vector2

import settings as Settings

from game.context import GameContext
from game.objects.dynamic_objects.dynamic_object import DynamicObject


class Projectile(DynamicObject):
    __slots__ = ("damage",)

    damage: int


    def __init__(
        self,
        context: GameContext,
        damage: int,
        position: Vector2,
        velocity: Vector2,
    ) -> None:
        super().__init__(context, position, velocity)
        self.collision_layer = Settings.PROJECTILE
        self.collidable = False
        self.radius = 4
        self.position_z = -22.0
        self.height = 8
        self.damage = damage


    def update(self, delta: float) -> None:
        self._move_and_slide(delta)

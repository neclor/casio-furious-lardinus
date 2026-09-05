from gamekit.math.vectors.vector2 import Vector2

import settings as Settings

from game.context import GameContext
from game.objects.game_object import GameObject


class ActiveObject(GameObject):
    __slots__ = ()


    def __init__(self, context: GameContext, position: Vector2) -> None:
        super().__init__(context, position)
        self.collision_layer = Settings.ACTIVE
        self.collision_mask = Settings.PLAYER
        self.radius = 12
        self.position_z = 0.0
        self.height = 24

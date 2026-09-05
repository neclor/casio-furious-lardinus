from gamekit.math.vectors.vector2 import Vector2
import settings as Settings
from flgame.context import GameContext
from flgame.objects.game_object import GameObject

class ActiveObject(GameObject):
    __slots__ = ()

    def __init__(self, context, position):
        super().__init__(context, position)
        self.collision_layer = Settings.ACTIVE
        self.collision_mask = Settings.PLAYER
        self.radius = 12
        self.position_z = 0.0
        self.height = 24

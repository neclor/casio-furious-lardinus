from gamekit.math.vectors.vector2 import Vector2
from flgame.context import GameContext
from flgame.objects.game_object import GameObject

class DynamicObject(GameObject):
    __slots__ = ('velocity',)

    def __init__(self, context, position, velocity=None):
        super().__init__(context, position)
        self.static = False
        self.velocity = Vector2(velocity) if velocity is not None else Vector2()

    def _move_and_slide(self, delta):
        self.position += self.velocity * delta

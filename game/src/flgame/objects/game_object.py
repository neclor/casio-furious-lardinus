from gamekit.math.vectors.vector2 import Vector2
from flgame.context import GameContext
from flgame.levels.tiles import Tile

class GameObject:
    __slots__ = ('context', 'freed', 'collision_layer', 'collision_mask', 'collidable', 'static', 'position', 'radius', 'position_z', 'height', 'sprite')

    def __init__(self, context, position):
        self.context = context
        self.freed = False
        self.collision_layer = 0
        self.collision_mask = 0
        self.collidable = False
        self.static = True
        self.position = Vector2(position)
        self.radius = 16
        self.position_z = 0.0
        self.height = 32
        self.sprite = None

    def update(self, delta):
        pass

    def on_collision(self, other):
        pass

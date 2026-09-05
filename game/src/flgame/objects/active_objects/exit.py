
import systems.services as services
from gamekit.math.vectors.vector2 import Vector2

from flgame.context import GameContext
from flgame.objects.active_objects.active_object import ActiveObject
from flgame.objects.dynamic_objects.entities.player import Player
from flgame.objects.game_object import GameObject
from flgame.levels.tiles import Tile


class Exit(ActiveObject):
    __slots__ = ()


    def __init__(self, context: GameContext, position: Vector2) -> None:
        super().__init__(context, position)
        self.radius = 16
        self.position_z = 0.0
        self.height = 64
        self.sprite = services.renderer.load_texture("src/assets/sprites/objects/exit.png")


    def on_collision(self, other: GameObject | Tile) -> None:
        if isinstance(other, Player):
            self.context.level.next()

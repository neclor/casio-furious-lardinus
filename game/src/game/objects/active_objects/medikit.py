
from gamekit.systems.render.texture import Texture
from systems.services import services
from gamekit.math.vectors import Vector2

from game.context import GameContext
from game.objects.active_objects.active_object import ActiveObject
from game.objects.dynamic_objects.entities.player import Player
from game.objects.game_object import GameObject
from game.levels.tiles import Tile


_SPRITE: Texture = services.renderer.load_texture("src/assets/sprites/objects/medikit_16.png")
_HEAL_AMOUNT: int = 25


class Medikit(ActiveObject):
    __slots__ = ()


    def __init__(self, context: GameContext, position: Vector2) -> None:
        super().__init__(context, position)
        self.sprite = _SPRITE


    def on_collision(self, other: GameObject | Tile) -> None:
        if isinstance(other, Player) and other.health < other.max_health:
            other.take_heal(_HEAL_AMOUNT)
            self.context.world.remove(self)

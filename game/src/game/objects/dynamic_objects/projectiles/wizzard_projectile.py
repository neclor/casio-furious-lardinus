
from gamekit.systems.render.texture import Texture
from systems.services import services
from gamekit.math.vectors import Vector2

import settings as Settings

from game.context import GameContext
from game.objects.dynamic_objects.projectiles.projectile import Projectile
from game.objects.dynamic_objects.entities.player import Player
from game.objects.game_object import GameObject
from game.levels.tiles import Tile


_SPRITE: Texture = services.renderer.load_texture(
    "src/assets/sprites/projectiles/wizzard_projectile_16.png"
)


class WizzardProjectile(Projectile):
    __slots__ = ()


    def __init__(
        self,
        context: GameContext,
        damage: int,
        position: Vector2,
        velocity: Vector2,
    ) -> None:
        super().__init__(context, damage, position, velocity)
        self.collision_mask = Settings.WALL | Settings.PLAYER
        self.radius = 8
        self.position_z = -8.0
        self.height = 16
        self.sprite = _SPRITE


    def on_collision(self, other: GameObject | Tile) -> None:
        if isinstance(other, Tile):
            self.context.world.remove(self)
        elif isinstance(other, Player):
            other.take_damage(self.damage)
            self.context.world.remove(self)

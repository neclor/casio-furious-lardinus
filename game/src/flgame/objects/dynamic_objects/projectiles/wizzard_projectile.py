
import systems.services as services
from gamekit.math.vectors.vector2 import Vector2

import settings as Settings

from flgame.context import GameContext
from flgame.objects.dynamic_objects.projectiles.projectile import Projectile
from flgame.objects.dynamic_objects.entities.player import Player
from flgame.objects.game_object import GameObject
from flgame.levels.tiles import Tile


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
        self.sprite = services.renderer.load_texture("src/assets/sprites/projectiles/wizzard_projectile_16.png")


    def on_collision(self, other: GameObject | Tile) -> None:
        if isinstance(other, Tile):
            self.context.world.remove(self)
        elif isinstance(other, Player):
            other.take_damage(self.damage)
            self.context.world.remove(self)

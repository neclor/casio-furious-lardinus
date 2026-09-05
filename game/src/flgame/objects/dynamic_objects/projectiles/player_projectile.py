import systems.services as services
from gamekit.math.vectors.vector2 import Vector2
import settings as Settings
from flgame.context import GameContext
from flgame.objects.dynamic_objects.projectiles.projectile import Projectile
from flgame.objects.dynamic_objects.entities.enemies.enemy import Enemy
from flgame.levels.tiles import Tile

class PlayerProjectile(Projectile):
    __slots__ = ()

    def __init__(self, context, damage, position, velocity):
        super().__init__(context, damage, position, velocity)
        self.collision_mask = Settings.WALL | Settings.ENEMY
        self.sprite = services.renderer.load_texture('src/assets/sprites/projectiles/player_projectile_4.png')

    def on_collision(self, other):
        if isinstance(other, Tile):
            self.context.world.remove(self)
        elif isinstance(other, Enemy):
            other.take_damage(self.damage)
            self.context.world.remove(self)


from gamekit.systems.render.texture import Texture
from systems.services import services
from gamekit.math.vectors import Vector2

import settings as Settings

from game.context import GameContext
from game.objects.dynamic_objects.entities.enemies.enemy import Enemy
from game.objects.dynamic_objects.entities.player import Player
from game.objects.game_object import GameObject
from game.levels.tiles import Tile


_SPRITE: Texture = services.renderer.load_texture("src/assets/sprites/enemies/skull_32.png")


class Skull(Enemy):
    __slots__ = ()


    def __init__(self, context: GameContext, position: Vector2) -> None:
        super().__init__(context, position)
        self.collision_layer = Settings.ENEMY
        self.collision_mask = Settings.WALL | Settings.PLAYER
        self.collidable = False

        self.position_z = -32.0
        self.height = 32
        self.sprite = _SPRITE
        self.speed = 128
        self.max_health = 50
        self.health = 50
        self.attack_range = 0
        self.damage = 5


    def on_collision(self, other: GameObject | Tile) -> None:
        if isinstance(other, Tile):
            self.die()
        elif isinstance(other, Player):
            other.take_damage(self.damage)
            self.die()


from gamekit.systems.render.texture import Texture
from systems.services import services
from gamekit.math.vectors import Vector2

from game.context import GameContext
from game.objects.dynamic_objects.entities.enemies.enemy import Enemy
from game.objects.active_objects.medikit import Medikit


_SPRITE: Texture = services.renderer.load_texture("src/assets/sprites/enemies/knight_32_48.png")


class Knight(Enemy):
    __slots__ = ()


    def __init__(self, context: GameContext, position: Vector2) -> None:
        super().__init__(context, position)
        self.position_z = -16.0
        self.height = 48
        self.sprite = _SPRITE
        self.speed = 96
        self.max_health = 200
        self.health = 200
        self.attack_cooldown = 1.0
        self.attack_range = 32
        self.damage = 5


    def attack(self) -> None:
        self.context.player.take_damage(self.damage)


    def _drop_loot(self) -> None:
        self.context.world.add(Medikit(self.context, self.position.copy()))


from systems.services import services
from gamekit.math.vectors.vector2 import Vector2

from game.context import GameContext
from game.objects.dynamic_objects.entities.enemies.enemy import Enemy
from game.objects.dynamic_objects.entities.enemies.skull import Skull
from game.objects.active_objects.ammo import Ammo
from game.objects.active_objects.medikit import Medikit


class Boss(Enemy):
    __slots__ = ()


    def __init__(self, context: GameContext, position: Vector2) -> None:
        super().__init__(context, position)
        self.position_z = 0.0
        self.height = 128
        self.sprite = services.renderer.load_texture("src/assets/sprites/enemies/boss_128.png")
        self.speed = 96
        self.max_health = 500
        self.health = 500
        self.attack_cooldown = 2.0
        self.attack_range = 128
        self.damage = 20


    def attack(self) -> None:
        self.context.player.take_damage(self.damage)
        self.context.world.add(Skull(self.context, self.position.copy()))


    def _drop_loot(self) -> None:
        world = self.context.world
        world.add(Medikit(self.context, self.position.copy()))
        world.add(Ammo(self.context, self.position.copy()))
        world.add(Skull(self.context, self.position.copy()))

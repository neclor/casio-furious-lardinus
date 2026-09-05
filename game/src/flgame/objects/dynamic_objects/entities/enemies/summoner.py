import systems.services as services
from gamekit.math.vectors.vector2 import Vector2
from flgame.context import GameContext
from flgame.objects.dynamic_objects.entities.enemies.enemy import Enemy

class Summoner(Enemy):
    __slots__ = ()

    def __init__(self, context, position):
        super().__init__(context, position)
        self.position_z = 0.0
        self.height = 48
        self.sprite = services.renderer.load_texture('src/assets/sprites/enemies/summoner_8_12.png')
        self.speed = 32
        self.max_health = 100
        self.health = 100
        self.attack_cooldown = 5.0
        self.attack_range = 1024

    def attack(self):
        from flgame.objects.dynamic_objects.entities.enemies.skull import Skull
        self.context.world.add(Skull(self.context, self.position.copy()))

    def _drop_loot(self):
        from flgame.objects.active_objects.ammo import Ammo
        self.context.world.add(Ammo(self.context, self.position.copy()))

import systems.services as services
from gamekit.math.vectors.vector2 import Vector2
from flgame.context import GameContext
from flgame.objects.dynamic_objects.entities.enemies.enemy import Enemy
_PROJECTILE_SPEED = 192

class Wizzard(Enemy):
    __slots__ = ()

    def __init__(self, context, position):
        super().__init__(context, position)
        self.position_z = 0.0
        self.height = 48
        self.sprite = services.renderer.load_texture('src/assets/sprites/enemies/wizzard_8_12.png')
        self.speed = 32
        self.max_health = 100
        self.health = 100
        self.attack_cooldown = 2.0
        self.attack_range = 1024
        self.damage = 10

    def attack(self):
        vector_to_player = self.context.player.position - self.position
        if vector_to_player.length() > 0:
            from flgame.objects.dynamic_objects.projectiles.wizzard_projectile import WizzardProjectile
            self.context.world.add(WizzardProjectile(self.context, self.damage, self.position.copy(), vector_to_player.normalized() * _PROJECTILE_SPEED))

    def _drop_loot(self):
        from flgame.objects.active_objects.ammo import Ammo
        self.context.world.add(Ammo(self.context, self.position.copy()))

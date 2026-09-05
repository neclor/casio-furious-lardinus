import random

from gamekit.math.vectors.vector2 import Vector2

import settings as Settings

import systems.services as services
from actions import Actions
from game.context import GameContext
from game.weapons.weapon import Weapon
from game.objects.dynamic_objects.projectiles.player_projectile import PlayerProjectile


_PROJECTILE_SPEED: int = 320


class WeaponManager:
    __slots__ = ("context", "gun", "shotgun", "assault", "current", "_cooldown_left")

    context: GameContext
    gun: Weapon
    shotgun: Weapon
    assault: Weapon
    current: Weapon
    _cooldown_left: float


    def __init__(self, context: GameContext) -> None:
        self.context = context
        self.gun = Weapon("Gun", damage=20, max_ammo=float("inf"), cooldown=0.3)
        self.shotgun = Weapon("Shotgun", damage=30, max_ammo=100, cooldown=0.5)
        self.assault = Weapon("Assault Rifle", damage=15, max_ammo=200, cooldown=0.1)
        self.current = self.gun
        self._cooldown_left = 0.0


    def update(self, delta: float) -> None:
        self._cooldown_left = max(self._cooldown_left - delta, 0.0)
        self._handle_events()
        if self.current is self.assault and Actions.FIRE.is_down(services.input):
            self._shoot()


    def add_ammo(self, amount: int) -> bool:
        received = False
        if self.shotgun.available and self.shotgun.ammo < self.shotgun.max_ammo:
            self.shotgun.ammo = min(self.shotgun.ammo + amount, self.shotgun.max_ammo)
            received = True
        if self.assault.available and self.assault.ammo < self.assault.max_ammo:
            self.assault.ammo = min(
                self.assault.ammo + amount * 2, self.assault.max_ammo
            )
            received = True
        return received


    def change_weapon(self, weapon: Weapon) -> None:
        if weapon is self.current or not weapon.available:
            return
        self.current = weapon
        self._cooldown_left = weapon.cooldown


    def _handle_events(self) -> None:
        if Actions.FIRE.is_pressed(services.input):
            self._shoot()

        if Actions.WEAPON_GUN.is_pressed(services.input):
            self.change_weapon(self.gun)
        elif Actions.WEAPON_SHOTGUN.is_pressed(services.input):
            self.change_weapon(self.shotgun)
        elif Actions.WEAPON_ASSAULT.is_pressed(services.input):
            self.change_weapon(self.assault)


    def _shoot(self) -> None:
        if self._cooldown_left > 0 or self.current.ammo <= 0:
            return
        self.current.ammo -= 1
        self._cooldown_left = self.current.cooldown

        if self.current is self.gun:
            self._fire(0.0)
        elif self.current is self.shotgun:
            for _ in range(5):
                self._fire(random.uniform(-Settings.HALF_PI / 4, Settings.HALF_PI / 4))
        else:
            self._fire(random.uniform(-0.1, 0.1))


    def _fire(self, spread: float) -> None:
        player = self.context.player
        velocity = Vector2(_PROJECTILE_SPEED, 0).rotated(
            player.rotation + spread
        )
        self.context.world.add(
            PlayerProjectile(
                self.context, self.current.damage, player.position.copy(), velocity
            )
        )

import math

from gamekit.math.vectors import Vector2

import settings as Settings

from gamekit.systems.actions import get_axis

from systems.services import services
from actions import Actions
from game.context import GameContext
from game.objects.dynamic_objects.entities.entity import Entity


_VELOCITY_INERTIA_FACTOR: int = 4
_BOBBING_AMPLITUDE: float = 1.0
_BOBBING_SPEED: float = 0.1
_TURN_SPEED: float = 3.0


class Player(Entity):
    __slots__ = ("rotation", "bobbing_timer")

    rotation: float
    bobbing_timer: float


    def __init__(self, context: GameContext, position: Vector2) -> None:
        super().__init__(context, position)
        self.collision_layer = Settings.PLAYER
        self.collision_mask = Settings.WALL | Settings.OBSTACLE | Settings.ENEMY

        self.rotation = 0.0
        self.speed = 128
        self.bobbing_timer = 0.0

        self.max_health = 100
        self.health = 100
        self.height = 32


    def update(self, delta: float) -> None:
        self._move(delta)
        self._rotate(delta)
        self._bob(delta)


    def die(self) -> None:
        self.dead = True
        self.context.level.load()
        self.health = self.max_health
        self.dead = False


    def _move(self, delta: float) -> None:
        input_direction: Vector2 = Vector2(
            get_axis(Actions.MOVE_LEFT, Actions.MOVE_RIGHT, services.input),
            get_axis(Actions.MOVE_FORWARD, Actions.MOVE_BACKWARD, services.input),
        )

        move_direction: Vector2 = Vector2()
        if input_direction.x != 0 or input_direction.y != 0:
            move_direction = input_direction.rotated(
                self.rotation + Settings.HALF_PI
            ).normalized()

        self.velocity = self.velocity.lerp(
            move_direction * self.speed,
            min(delta * _VELOCITY_INERTIA_FACTOR, 1),
        )
        self._move_and_slide(delta)


    def _rotate(self, delta: float) -> None:
        rel_x: float = services.input.mouse_delta().x
        turn: float = get_axis(Actions.TURN_LEFT, Actions.TURN_RIGHT, services.input)
        yaw: float = (
            (rel_x / Settings.resolution[0] / 4)
            * Settings.fov_h
            * Settings.camera_sensitivity
            + turn * _TURN_SPEED * delta
        )
        self.rotation = (self.rotation + yaw) % (2 * math.pi)


    def _bob(self, delta: float) -> None:
        self.bobbing_timer = (
            self.bobbing_timer
            + self.velocity.length() * _BOBBING_SPEED * delta
        ) % (2 * math.pi)
        self.position_z = math.sin(self.bobbing_timer) * _BOBBING_AMPLITUDE

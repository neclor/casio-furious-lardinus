import math
from gamekit.math.vectors.vector2 import Vector2
import settings as Settings
from gamekit.systems.actions import get_axis
import systems.services as services
from actions import Actions
from flgame.context import GameContext
from flgame.objects.dynamic_objects.entities.entity import Entity
_VELOCITY_INERTIA_FACTOR = 4
_BOBBING_AMPLITUDE = 1.0
_BOBBING_SPEED = 0.1
_TURN_SPEED = 3.0

class Player(Entity):
    __slots__ = ('rotation', 'bobbing_timer')

    def __init__(self, context, position):
        super().__init__(context, position)
        self.collision_layer = Settings.PLAYER
        self.collision_mask = Settings.WALL | Settings.OBSTACLE | Settings.ENEMY
        self.rotation = 0.0
        self.speed = 128
        self.bobbing_timer = 0.0
        self.max_health = 100
        self.health = 100
        self.height = 32

    def update(self, delta):
        self._move(delta)
        self._rotate(delta)
        self._bob(delta)

    def die(self):
        self.dead = True
        self.context.level.load()
        self.health = self.max_health
        self.dead = False

    def _move(self, delta):
        input_direction = Vector2(get_axis(Actions.MOVE_LEFT, Actions.MOVE_RIGHT, services.input), get_axis(Actions.MOVE_FORWARD, Actions.MOVE_BACKWARD, services.input))
        move_direction = Vector2()
        if input_direction.x != 0 or input_direction.y != 0:
            move_direction = input_direction.rotated(self.rotation + Settings.HALF_PI).normalized()
        self.velocity = self.velocity.lerp(move_direction * self.speed, min(delta * _VELOCITY_INERTIA_FACTOR, 1))
        self._move_and_slide(delta)

    def _rotate(self, delta):
        turn = get_axis(Actions.TURN_LEFT, Actions.TURN_RIGHT, services.input)
        self.rotation = (self.rotation + turn * _TURN_SPEED * delta) % (2 * math.pi)

    def _bob(self, delta):
        self.bobbing_timer = (self.bobbing_timer + self.velocity.length() * _BOBBING_SPEED * delta) % (2 * math.pi)
        self.position_z = math.sin(self.bobbing_timer) * _BOBBING_AMPLITUDE

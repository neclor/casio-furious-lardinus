TYPE_CHECKING = False

from gamekit.math.vectors.vector2 import Vector2

import settings as Settings

from game.context import GameContext
from game.objects.dynamic_objects.entities.entity import Entity

if TYPE_CHECKING:
    from game.levels.level import Level
    from game.levels.tiles import Tile
    from game.objects.dynamic_objects.entities.player import Player


class Enemy(Entity):
    __slots__ = ("attack_cooldown", "attack_cooldown_left", "attack_range", "damage")

    attack_cooldown: float
    attack_cooldown_left: float
    attack_range: int
    damage: int


    def __init__(self, context: GameContext, position: Vector2) -> None:
        super().__init__(context, position)
        self.collision_layer = Settings.ENEMY
        self.collision_mask = (
            Settings.WALL | Settings.OBSTACLE | Settings.ENEMY | Settings.PLAYER
        )
        self.height = 48

        self.attack_cooldown = 1.0
        self.attack_cooldown_left = 0.0
        self.attack_range = 64
        self.damage = 10


    def update(self, delta: float) -> None:
        self.velocity = Vector2()
        self.attack_cooldown_left = max(0.0, self.attack_cooldown_left - delta)
        if not self._see_player():
            return
        self._move_and_attack()
        self._move_and_slide(delta)


    def die(self) -> None:
        self._drop_loot()
        super().die()


    def attack(self) -> None:
        pass


    def _drop_loot(self) -> None:
        pass


    def _move_and_attack(self) -> None:
        player: "Player" = self.context.player
        vector_to_player: Vector2 = player.position - self.position
        distance: float = vector_to_player.length()

        if distance > self.attack_range + player.radius:
            self.velocity = vector_to_player.normalized() * self.speed
        elif self.attack_cooldown_left == 0:
            self.attack_cooldown_left = self.attack_cooldown
            self.attack()


    def _see_player(self) -> bool:
        level: "Level" = self.context.level
        tile_size: Vector2 = level.tile_size
        map_size: Vector2 = level.tile_map_size

        x: int = int(self.position.x // tile_size.x)
        y: int = int(self.position.y // tile_size.y)
        player_position: Vector2 = self.context.player.position
        player_x: int = int(player_position.x // tile_size.x)
        player_y: int = int(player_position.y // tile_size.y)

        ray_sign_x: int = 1 if x < player_x else (-1 if x > player_x else 0)
        ray_sign_y: int = 1 if y < player_y else (-1 if y > player_y else 0)
        abs_delta_x: int = abs(x - player_x)
        abs_delta_y: int = abs(y - player_y)

        error: int = abs_delta_x - abs_delta_y
        while True:
            if not (0 <= x < map_size.x and 0 <= y < map_size.y):
                return False
            tile: "Tile | None" = level.tile_map[y][x]
            if tile is not None and (tile.collision_layer & Settings.WALL) > 0:
                return False
            if x == player_x and y == player_y:
                return True
            if error >= 0:
                error -= abs_delta_y
                x += ray_sign_x
            if error <= 0:
                error += abs_delta_x
                y += ray_sign_y

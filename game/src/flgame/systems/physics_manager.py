TYPE_CHECKING = False

from gamekit.math.vectors.vector2 import Vector2
from gamekit.math.utils import clampf

from flgame.context import GameContext

if TYPE_CHECKING:
    from flgame.levels.level import Level
    from flgame.levels.tiles import Tile
    from flgame.objects.game_object import GameObject


def _detects(source: "GameObject | Tile", target: "GameObject | Tile") -> bool:
    return (source.collision_mask & target.collision_layer) > 0


class PhysicsManager:
    __slots__ = ("context",)

    context: GameContext


    def __init__(self, context: GameContext) -> None:
        self.context = context


    def resolve(self, objects: "list[GameObject]") -> None:
        i: int
        game_object: "GameObject"
        for i, game_object in enumerate(objects):
            if game_object.freed:
                continue
            other: "GameObject"
            for other in objects[i + 1:]:
                self._collide_pair(game_object, other)
            self._collide_tiles(game_object)


    def _collide_pair(self, a: "GameObject", b: "GameObject") -> None:
        detect_a: bool = _detects(a, b)
        detect_b: bool = _detects(b, a)
        if not (detect_a or detect_b):
            return

        vector: Vector2 = a.position - b.position
        distance: float = vector.length()
        overlap: float = a.radius + b.radius - distance
        if overlap <= 0:
            return

        if detect_a:
            a.on_collision(b)
        if detect_b:
            b.on_collision(a)

        if not (a.collidable and b.collidable):
            return
        if a.static and b.static:
            return
        if distance == 0:
            return

        push: Vector2 = vector.normalized() * overlap
        if b.static:
            a.position += push
        elif a.static:
            b.position -= push
        else:
            a.position += push / 2
            b.position -= push / 2


    def _collide_tiles(self, game_object: "GameObject") -> None:
        level: "Level" = self.context.level
        tile_size: Vector2 = level.tile_size
        position: Vector2 = game_object.position
        radius: int = game_object.radius

        min_x: int = int(max(0, (position.x - radius) // tile_size.x))
        max_x: int = int(min((position.x + radius) // tile_size.x,
                             level.tile_map_size.x - 1))
        min_y: int = int(max(0, (position.y - radius) // tile_size.y))
        max_y: int = int(min((position.y + radius) // tile_size.y,
                             level.tile_map_size.y - 1))

        ty: int
        tx: int
        for ty in range(min_y, max_y + 1):
            for tx in range(min_x, max_x + 1):
                tile: "Tile | None" = level.tile_map[ty][tx]
                if tile is None or not _detects(game_object, tile):
                    continue

                nearest: Vector2 = self._nearest_tile_point(
                    position, tx, ty, tile_size
                )
                vector: Vector2 = position - nearest
                distance: float = vector.length()
                overlap: float = radius - distance
                if overlap <= 0:
                    continue

                game_object.on_collision(tile)
                if not (game_object.collidable and tile.collidable):
                    continue
                if game_object.static or distance == 0:
                    continue
                game_object.position += vector.normalized() * overlap


    @staticmethod
    def _nearest_tile_point(
        position: Vector2, tx: int, ty: int, tile_size: Vector2
    ) -> Vector2:
        left: float = tx * tile_size.x
        top: float = ty * tile_size.y
        return Vector2(
            clampf(position.x, left, left + tile_size.x),
            clampf(position.y, top, top + tile_size.y),
        )

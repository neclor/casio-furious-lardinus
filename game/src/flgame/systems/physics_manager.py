from gamekit.math.utils import clampf
from gamekit.math.vectors.vector2 import Vector2

def _detects(source, target):
    return source.collision_mask & target.collision_layer > 0

class PhysicsManager:
    __slots__ = ('context',)

    def __init__(self, context):
        self.context = context

    def resolve(self, objects):
        for i, game_object in enumerate(objects):
            if game_object.freed:
                continue
            for other in objects[i + 1:]:
                self._collide_pair(game_object, other)
            self._collide_tiles(game_object)

    def _collide_pair(self, a, b):
        detect_a = _detects(a, b)
        detect_b = _detects(b, a)
        if not (detect_a or detect_b):
            return
        vector = a.position - b.position
        distance = vector.length()
        overlap = a.radius + b.radius - distance
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
        push = vector.normalized() * overlap
        if b.static:
            a.position += push
        elif a.static:
            b.position -= push
        else:
            a.position += push / 2
            b.position -= push / 2

    def _collide_tiles(self, game_object):
        level = self.context.level
        tile_size = level.tile_size
        position = game_object.position
        radius = game_object.radius
        min_x = int(max(0, (position.x - radius) // tile_size.x))
        max_x = int(min((position.x + radius) // tile_size.x, level.tile_map_size.x - 1))
        min_y = int(max(0, (position.y - radius) // tile_size.y))
        max_y = int(min((position.y + radius) // tile_size.y, level.tile_map_size.y - 1))
        for ty in range(min_y, max_y + 1):
            for tx in range(min_x, max_x + 1):
                tile = level.tile_map[ty][tx]
                if tile is None or not _detects(game_object, tile):
                    continue
                nearest = self._nearest_tile_point(position, tx, ty, tile_size)
                vector = position - nearest
                distance = vector.length()
                overlap = radius - distance
                if overlap <= 0:
                    continue
                game_object.on_collision(tile)
                if not (game_object.collidable and tile.collidable):
                    continue
                if game_object.static or distance == 0:
                    continue
                game_object.position += vector.normalized() * overlap

    @staticmethod
    def _nearest_tile_point(position, tx, ty, tile_size):
        left = tx * tile_size.x
        top = ty * tile_size.y
        return Vector2(clampf(position.x, left, left + tile_size.x), clampf(position.y, top, top + tile_size.y))

def _detects(source, target):
    return source.collision_mask & target.collision_layer > 0

class PhysicsManager:
    __slots__ = ('context', '_collide_tiles')

    def __init__(self, context):
        self.context = context
        import gc
        from flgame.systems.physics_tiles import collide_tiles
        self._collide_tiles = collide_tiles
        gc.collect()

    def resolve(self, objects):
        for i, game_object in enumerate(objects):
            if game_object.freed:
                continue
            for other in objects[i + 1:]:
                self._collide_pair(game_object, other)
            self._collide_tiles(game_object, self.context.level)

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

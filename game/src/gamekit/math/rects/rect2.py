from gamekit.math.vectors.vector2 import Vector2
from gamekit.math.rects.rect2i import Rect2i

class Rect2:
    __slots__ = ('position', 'size')

    def __init__(self, x=0.0, y=0.0, width=0.0, height=0.0):
        self.set(x, y, width, height)

    def set(self, x=0.0, y=0.0, width=0.0, height=0.0):
        if isinstance(x, (Rect2, Rect2i)):
            self.position = Vector2(x.position)
            self.size = Vector2(x.size)
        elif isinstance(x, (int, float)) and isinstance(y, (int, float)):
            self.position = Vector2(x, y)
            self.size = Vector2(width, height)
        else:
            self.position = Vector2(x)
            self.size = Vector2(y)
        return self

    def __eq__(self, o):
        return isinstance(o, Rect2) and self.position == o.position and (self.size == o.size)

    def __ne__(self, o):
        return not (isinstance(o, Rect2) and self.position == o.position and (self.size == o.size))

    def __hash__(self):
        return hash((self.position.x, self.position.y, self.size.x, self.size.y))

    def __repr__(self):
        return 'Rect2({}, {}, {}, {})'.format(self.position.x, self.position.y, self.size.x, self.size.y)

    def __str__(self):
        return '[P: {}, S: {}]'.format(self.position, self.size)

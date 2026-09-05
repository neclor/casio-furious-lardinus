from gamekit.math.vectors.vector2i import Vector2i

class Rect2i:
    __slots__ = ('position', 'size')

    def __init__(self, x=0, y=0, width=0, height=0):
        self.set(x, y, width, height)

    def set(self, x=0, y=0, width=0, height=0):
        from gamekit.math.rects.rect2 import Rect2
        if isinstance(x, (Rect2i, Rect2)):
            self.position = Vector2i(x.position)
            self.size = Vector2i(x.size)
        elif isinstance(x, (int, float)) and isinstance(y, (int, float)):
            self.position = Vector2i(int(x), int(y))
            self.size = Vector2i(int(width), int(height))
        else:
            self.position = Vector2i(x)
            self.size = Vector2i(y)
        return self

    def __eq__(self, o):
        return isinstance(o, Rect2i) and self.position == o.position and (self.size == o.size)

    def __ne__(self, o):
        return not (isinstance(o, Rect2i) and self.position == o.position and (self.size == o.size))

    def __hash__(self):
        return hash((self.position.x, self.position.y, self.size.x, self.size.y))

    def __repr__(self):
        return 'Rect2i({}, {}, {}, {})'.format(self.position.x, self.position.y, self.size.x, self.size.y)

    def __str__(self):
        return '[P: {}, S: {}]'.format(self.position, self.size)

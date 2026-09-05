from gamekit.math.utils import *

class Vector2i:
    __slots__ = ('x', 'y')

    def __init__(self, x=0, y=0):
        if isinstance(x, (int, float)):
            ix, iy = (int(x), int(y))
        elif isinstance(x, (tuple, list)):
            ix, iy = (int(x[0]), int(x[1]))
        else:
            ix, iy = (int(x.x), int(x.y))
        self.x = ix
        self.y = iy

    def __add__(self, o):
        return Vector2i(self.x + o.x, self.y + o.y)

    def __sub__(self, o):
        return Vector2i(self.x - o.x, self.y - o.y)

    def __mul__(self, o):
        if isinstance(o, Vector2i):
            return Vector2i(self.x * o.x, self.y * o.y)
        return Vector2i(self.x * o, self.y * o)

    def __rmul__(self, o):
        return Vector2i(self.x * o, self.y * o)

    def __truediv__(self, o):
        if isinstance(o, Vector2i):
            return Vector2i(idiv(self.x, o.x), idiv(self.y, o.y))
        return Vector2i(idiv(self.x, o), idiv(self.y, o))
    __floordiv__ = __truediv__

    def __mod__(self, o):
        if isinstance(o, Vector2i):
            return Vector2i(imod(self.x, o.x), imod(self.y, o.y))
        return Vector2i(imod(self.x, o), imod(self.y, o))

    def __iadd__(self, o):
        self.x += o.x
        self.y += o.y
        return self

    def __isub__(self, o):
        self.x -= o.x
        self.y -= o.y
        return self

    def __imul__(self, o):
        if isinstance(o, Vector2i):
            self.x *= o.x
            self.y *= o.y
        else:
            self.x *= o
            self.y *= o
        return self

    def __itruediv__(self, o):
        if isinstance(o, Vector2i):
            self.x = idiv(self.x, o.x)
            self.y = idiv(self.y, o.y)
        else:
            self.x = idiv(self.x, o)
            self.y = idiv(self.y, o)
        return self
    __ifloordiv__ = __itruediv__

    def __imod__(self, o):
        if isinstance(o, Vector2i):
            self.x = imod(self.x, o.x)
            self.y = imod(self.y, o.y)
        else:
            self.x = imod(self.x, o)
            self.y = imod(self.y, o)
        return self

    def __neg__(self):
        return Vector2i(-self.x, -self.y)

    def __pos__(self):
        return Vector2i(self.x, self.y)

    def __abs__(self):
        return Vector2i(abs(self.x), abs(self.y))

    def __eq__(self, o):
        return isinstance(o, Vector2i) and self.x == o.x and (self.y == o.y)

    def __ne__(self, o):
        return not (isinstance(o, Vector2i) and self.x == o.x and (self.y == o.y))

    def __hash__(self):
        return hash((self.x, self.y))

    def __lt__(self, o):
        return self.y < o.y if self.x == o.x else self.x < o.x

    def __le__(self, o):
        return self.y <= o.y if self.x == o.x else self.x < o.x

    def __gt__(self, o):
        return self.y > o.y if self.x == o.x else self.x > o.x

    def __ge__(self, o):
        return self.y >= o.y if self.x == o.x else self.x > o.x

    def __getitem__(self, i):
        if i == 0:
            return self.x
        if i == 1:
            return self.y
        raise IndexError('Vector2i index out of range')

    def __setitem__(self, i, value):
        if i == 0:
            self.x = int(value)
        elif i == 1:
            self.y = int(value)
        else:
            raise IndexError('Vector2i index out of range')

    def __len__(self):
        return 2

    def __iter__(self):
        yield self.x
        yield self.y

    def __bool__(self):
        return self.x != 0 or self.y != 0

    def __repr__(self):
        return 'Vector2i({}, {})'.format(self.x, self.y)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)
Vector2i.ZERO = Vector2i(0, 0)
Vector2i.ONE = Vector2i(1, 1)
Vector2i.MIN = Vector2i(INT_MIN, INT_MIN)
Vector2i.MAX = Vector2i(INT_MAX, INT_MAX)
Vector2i.LEFT = Vector2i(-1, 0)
Vector2i.RIGHT = Vector2i(1, 0)
Vector2i.UP = Vector2i(0, -1)
Vector2i.DOWN = Vector2i(0, 1)

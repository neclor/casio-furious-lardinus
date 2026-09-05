import math
from gamekit.math.utils import *

class Vector2:
    __slots__ = ('x', 'y')

    def __init__(self, x=0.0, y=0.0):
        if isinstance(x, (int, float)):
            fx, fy = (float(x), float(y))
        elif isinstance(x, (tuple, list)):
            fx, fy = (float(x[0]), float(x[1]))
        else:
            fx, fy = (float(x.x), float(x.y))
        self.x = fx
        self.y = fy

    def copy(self):
        return Vector2(self.x, self.y)

    def set(self, x, y):
        self.x = float(x)
        self.y = float(y)
        return self

    def ceil(self):
        return Vector2(math.ceil(self.x), math.ceil(self.y))

    def exp(self):
        return Vector2(math.exp(self.x), math.exp(self.y))

    def floor(self):
        return Vector2(math.floor(self.x), math.floor(self.y))

    def is_equal_approx(self, to):
        return is_equal_approx(self.x, to.x) and is_equal_approx(self.y, to.y)

    def is_finite(self):
        return math.isfinite(self.x) and math.isfinite(self.y)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def lerp(self, to, weight):
        return Vector2(lerp(self.x, to.x, weight), lerp(self.y, to.y, weight))

    def normalized(self):
        l = self.length()
        if l == 0.0:
            return Vector2(0.0, 0.0)
        return Vector2(self.x / l, self.y / l)

    def rotated(self, angle):
        c = math.cos(angle)
        s = math.sin(angle)
        return Vector2(self.x * c - self.y * s, self.x * s + self.y * c)

    def round(self):
        return Vector2(round_half_away(self.x), round_half_away(self.y))

    def __add__(self, o):
        return Vector2(self.x + o.x, self.y + o.y)

    def __sub__(self, o):
        return Vector2(self.x - o.x, self.y - o.y)

    def __mul__(self, o):
        if isinstance(o, Vector2):
            return Vector2(self.x * o.x, self.y * o.y)
        return Vector2(self.x * o, self.y * o)

    def __rmul__(self, o):
        return Vector2(self.x * o, self.y * o)

    def __truediv__(self, o):
        if isinstance(o, Vector2):
            return Vector2(self.x / o.x, self.y / o.y)
        return Vector2(self.x / o, self.y / o)

    def __iadd__(self, o):
        self.x += o.x
        self.y += o.y
        return self

    def __isub__(self, o):
        self.x -= o.x
        self.y -= o.y
        return self

    def __imul__(self, o):
        if isinstance(o, Vector2):
            self.x *= o.x
            self.y *= o.y
        else:
            self.x *= o
            self.y *= o
        return self

    def __itruediv__(self, o):
        if isinstance(o, Vector2):
            self.x /= o.x
            self.y /= o.y
        else:
            self.x /= o
            self.y /= o
        return self

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __pos__(self):
        return Vector2(self.x, self.y)

    def __abs__(self):
        return Vector2(abs(self.x), abs(self.y))

    def __round__(self):
        return self.round()

    def __floor__(self):
        return self.floor()

    def __ceil__(self):
        return self.ceil()

    def __eq__(self, o):
        return isinstance(o, Vector2) and self.x == o.x and (self.y == o.y)

    def __ne__(self, o):
        return not (isinstance(o, Vector2) and self.x == o.x and (self.y == o.y))

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
        raise IndexError('Vector2 index out of range')

    def __setitem__(self, i, value):
        if i == 0:
            self.x = float(value)
        elif i == 1:
            self.y = float(value)
        else:
            raise IndexError('Vector2 index out of range')

    def __len__(self):
        return 2

    def __iter__(self):
        yield self.x
        yield self.y

    def __bool__(self):
        return self.x != 0.0 or self.y != 0.0

    def __repr__(self):
        return 'Vector2({}, {})'.format(self.x, self.y)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)
Vector2.ZERO = Vector2(0.0, 0.0)
Vector2.ONE = Vector2(1.0, 1.0)
Vector2.INF = Vector2(float('inf'), float('inf'))
Vector2.LEFT = Vector2(-1.0, 0.0)
Vector2.RIGHT = Vector2(1.0, 0.0)
Vector2.UP = Vector2(0.0, -1.0)
Vector2.DOWN = Vector2(0.0, 1.0)

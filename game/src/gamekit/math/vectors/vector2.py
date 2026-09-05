import math

from gamekit.math.utils import *

TYPE_CHECKING = False

if TYPE_CHECKING:
    from collections.abc import Iterator
    from gamekit.math.vectors.vector2i import Vector2i


class Vector2:
    __slots__ = ("x", "y")

    x: float
    y: float

    ZERO: "Vector2"
    ONE: "Vector2"
    INF: "Vector2"
    LEFT: "Vector2"
    RIGHT: "Vector2"
    UP: "Vector2"
    DOWN: "Vector2"

    def __init__(
        self,
        x: "Vector2 | Vector2i | tuple[float, float] | list[float] | float" = 0.0,
        y: float = 0.0,
    ) -> None:
        if isinstance(x, (int, float)):
            fx, fy = float(x), float(y)
        elif isinstance(x, (tuple, list)):
            fx, fy = float(x[0]), float(x[1])
        else:
            fx, fy = float(x.x), float(x.y)
        self.x = fx
        self.y = fy

    def copy(self) -> "Vector2": return Vector2(self.x, self.y)

    def set(self, x: float, y: float) -> "Vector2":
        self.x = float(x)
        self.y = float(y)
        return self

    def ceil(self) -> "Vector2": return Vector2(math.ceil(self.x), math.ceil(self.y))

    def exp(self) -> "Vector2": return Vector2(math.exp(self.x), math.exp(self.y))

    def floor(self) -> "Vector2": return Vector2(math.floor(self.x), math.floor(self.y))

    def is_equal_approx(self, to: "Vector2") -> bool: return is_equal_approx(self.x, to.x) and is_equal_approx(self.y, to.y)

    def is_finite(self) -> bool: return math.isfinite(self.x) and math.isfinite(self.y)

    def length(self) -> float: return math.sqrt(self.x * self.x + self.y * self.y)

    def lerp(self, to: "Vector2", weight: float) -> "Vector2": return Vector2(lerp(self.x, to.x, weight), lerp(self.y, to.y, weight))

    def normalized(self) -> "Vector2":
        l = self.length()
        if l == 0.0:
            return Vector2(0.0, 0.0)
        return Vector2(self.x / l, self.y / l)

    def rotated(self, angle: float) -> "Vector2":
        c = math.cos(angle)
        s = math.sin(angle)
        return Vector2(self.x * c - self.y * s, self.x * s + self.y * c)

    def round(self) -> "Vector2": return Vector2(round_half_away(self.x), round_half_away(self.y))

    def __add__(self, o: "Vector2") -> "Vector2": return Vector2(self.x + o.x, self.y + o.y)

    def __sub__(self, o: "Vector2") -> "Vector2": return Vector2(self.x - o.x, self.y - o.y)

    def __mul__(self, o: "Vector2 | float") -> "Vector2":
        if isinstance(o, Vector2):
            return Vector2(self.x * o.x, self.y * o.y)
        return Vector2(self.x * o, self.y * o)

    def __rmul__(self, o: float) -> "Vector2": return Vector2(self.x * o, self.y * o)

    def __truediv__(self, o: "Vector2 | float") -> "Vector2":
        if isinstance(o, Vector2):
            return Vector2(self.x / o.x, self.y / o.y)
        return Vector2(self.x / o, self.y / o)

    def __iadd__(self, o: "Vector2") -> "Vector2":
        self.x += o.x
        self.y += o.y
        return self

    def __isub__(self, o: "Vector2") -> "Vector2":
        self.x -= o.x
        self.y -= o.y
        return self

    def __imul__(self, o: "Vector2 | float") -> "Vector2":
        if isinstance(o, Vector2):
            self.x *= o.x
            self.y *= o.y
        else:
            self.x *= o
            self.y *= o
        return self

    def __itruediv__(self, o: "Vector2 | float") -> "Vector2":
        if isinstance(o, Vector2):
            self.x /= o.x
            self.y /= o.y
        else:
            self.x /= o
            self.y /= o
        return self

    def __neg__(self) -> "Vector2": return Vector2(-self.x, -self.y)
    def __pos__(self) -> "Vector2": return Vector2(self.x, self.y)
    def __abs__(self) -> "Vector2": return Vector2(abs(self.x), abs(self.y))
    def __round__(self) -> "Vector2": return self.round()
    def __floor__(self) -> "Vector2": return self.floor()
    def __ceil__(self) -> "Vector2": return self.ceil()

    def __eq__(self, o: object) -> bool: return isinstance(o, Vector2) and self.x == o.x and self.y == o.y

    def __ne__(self, o: object) -> bool: return not (isinstance(o, Vector2) and self.x == o.x and self.y == o.y)

    def __hash__(self) -> int: return hash((self.x, self.y))

    def __lt__(self, o: "Vector2") -> bool: return self.y < o.y if self.x == o.x else self.x < o.x

    def __le__(self, o: "Vector2") -> bool: return self.y <= o.y if self.x == o.x else self.x < o.x

    def __gt__(self, o: "Vector2") -> bool: return self.y > o.y if self.x == o.x else self.x > o.x

    def __ge__(self, o: "Vector2") -> bool: return self.y >= o.y if self.x == o.x else self.x > o.x

    def __getitem__(self, i: int) -> float:
        if i == 0:
            return self.x
        if i == 1:
            return self.y
        raise IndexError("Vector2 index out of range")

    def __setitem__(self, i: int, value: float) -> None:
        if i == 0:
            self.x = float(value)
        elif i == 1:
            self.y = float(value)
        else:
            raise IndexError("Vector2 index out of range")

    def __len__(self) -> int: return 2

    def __iter__(self) -> "Iterator[float]":
        yield self.x
        yield self.y

    def __bool__(self) -> bool: return self.x != 0.0 or self.y != 0.0

    def __repr__(self) -> str: return "Vector2({}, {})".format(self.x, self.y)

    def __str__(self) -> str: return "({}, {})".format(self.x, self.y)


Vector2.ZERO = Vector2(0.0, 0.0)
Vector2.ONE = Vector2(1.0, 1.0)
Vector2.INF = Vector2(float("inf"), float("inf"))
Vector2.LEFT = Vector2(-1.0, 0.0)
Vector2.RIGHT = Vector2(1.0, 0.0)
Vector2.UP = Vector2(0.0, -1.0)
Vector2.DOWN = Vector2(0.0, 1.0)

from gamekit.math.vectors.vector2 import Vector2
from gamekit.math.rects.rect2i import Rect2i

TYPE_CHECKING = False

if TYPE_CHECKING:
    from gamekit.math.vectors.vector2i import Vector2i


class Rect2:
    __slots__ = ("position", "size")

    position: Vector2
    size: Vector2

    SIDE_LEFT: int = 0
    SIDE_TOP: int = 1
    SIDE_RIGHT: int = 2
    SIDE_BOTTOM: int = 3

    def __init__(
        self,
        x: "Rect2 | Rect2i | Vector2 | Vector2i | tuple[float, float] | list[float] | float" = 0.0,
        y: "Vector2 | Vector2i | tuple[float, float] | list[float] | float" = 0.0,
        width: float = 0.0,
        height: float = 0.0,
    ) -> None: self.set(x, y, width, height)

    def set(
        self,
        x: "Rect2 | Rect2i | Vector2 | Vector2i | tuple[float, float] | list[float] | float" = 0.0,
        y: "Vector2 | Vector2i | tuple[float, float] | list[float] | float" = 0.0,
        width: float = 0.0,
        height: float = 0.0,
    ) -> "Rect2":
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

    def copy(self) -> "Rect2": return Rect2(self.position.x, self.position.y, self.size.x, self.size.y)

    @property
    def end(self) -> Vector2: return self.position + self.size

    @end.setter
    def end(self, value: Vector2) -> None: self.size = Vector2(value.x - self.position.x, value.y - self.position.y)

    def abs(self) -> "Rect2":
        return Rect2(self.position.x + min(self.size.x, 0.0),
                     self.position.y + min(self.size.y, 0.0),
                     abs(self.size.x), abs(self.size.y))

    def encloses(self, b: "Rect2") -> bool:
        return (b.position.x >= self.position.x
                and b.position.y >= self.position.y
                and b.position.x + b.size.x <= self.position.x + self.size.x
                and b.position.y + b.size.y <= self.position.y + self.size.y)

    def expand(self, to: Vector2) -> "Rect2":
        begin_x = self.position.x
        begin_y = self.position.y
        end_x = self.position.x + self.size.x
        end_y = self.position.y + self.size.y
        if to.x < begin_x:
            begin_x = to.x
        if to.y < begin_y:
            begin_y = to.y
        if to.x > end_x:
            end_x = to.x
        if to.y > end_y:
            end_y = to.y
        return Rect2(begin_x, begin_y, end_x - begin_x, end_y - begin_y)

    def get_area(self) -> float: return self.size.x * self.size.y

    def get_center(self) -> Vector2: return self.position + self.size * 0.5

    def grow(self, amount: float) -> "Rect2": return Rect2(self.position.x - amount, self.position.y - amount, self.size.x + amount * 2.0, self.size.y + amount * 2.0)

    def grow_individual(self, left: float, top: float, right: float, bottom: float) -> "Rect2": return Rect2(self.position.x - left, self.position.y - top, self.size.x + left + right, self.size.y + top + bottom)

    def grow_side(self, side: int, amount: float) -> "Rect2":
        return self.grow_individual(
            amount if side == Rect2.SIDE_LEFT else 0.0,
            amount if side == Rect2.SIDE_TOP else 0.0,
            amount if side == Rect2.SIDE_RIGHT else 0.0,
            amount if side == Rect2.SIDE_BOTTOM else 0.0)

    def has_area(self) -> bool: return self.size.x > 0.0 and self.size.y > 0.0

    def has_point(self, point: Vector2) -> bool:
        if point.x < self.position.x:
            return False
        if point.y < self.position.y:
            return False
        if point.x >= self.position.x + self.size.x:
            return False
        if point.y >= self.position.y + self.size.y:
            return False
        return True

    def intersection(self, b: "Rect2") -> "Rect2":
        if not self.intersects(b):
            return Rect2()
        pos_x = max(b.position.x, self.position.x)
        pos_y = max(b.position.y, self.position.y)
        b_end_x = b.position.x + b.size.x
        b_end_y = b.position.y + b.size.y
        end_x = self.position.x + self.size.x
        end_y = self.position.y + self.size.y
        return Rect2(pos_x, pos_y, min(b_end_x, end_x) - pos_x, min(b_end_y, end_y) - pos_y)

    def intersects(self, b: "Rect2", include_borders: bool = False) -> bool:
        if include_borders:
            if self.position.x > b.position.x + b.size.x:
                return False
            if self.position.x + self.size.x < b.position.x:
                return False
            if self.position.y > b.position.y + b.size.y:
                return False
            if self.position.y + self.size.y < b.position.y:
                return False
        else:
            if self.position.x >= b.position.x + b.size.x:
                return False
            if self.position.x + self.size.x <= b.position.x:
                return False
            if self.position.y >= b.position.y + b.size.y:
                return False
            if self.position.y + self.size.y <= b.position.y:
                return False
        return True

    def is_equal_approx(self, rect: "Rect2") -> bool: return self.position.is_equal_approx(rect.position) and self.size.is_equal_approx(rect.size)

    def is_finite(self) -> bool: return self.position.is_finite() and self.size.is_finite()

    def merge(self, b: "Rect2") -> "Rect2":
        pos_x = min(b.position.x, self.position.x)
        pos_y = min(b.position.y, self.position.y)
        end_x = max(b.position.x + b.size.x, self.position.x + self.size.x)
        end_y = max(b.position.y + b.size.y, self.position.y + self.size.y)
        return Rect2(pos_x, pos_y, end_x - pos_x, end_y - pos_y)

    def __eq__(self, o: object) -> bool: return isinstance(o, Rect2) and self.position == o.position and self.size == o.size

    def __ne__(self, o: object) -> bool: return not (isinstance(o, Rect2) and self.position == o.position and self.size == o.size)

    def __hash__(self) -> int: return hash((self.position.x, self.position.y, self.size.x, self.size.y))

    def __repr__(self) -> str: return "Rect2({}, {}, {}, {})".format(self.position.x, self.position.y, self.size.x, self.size.y)

    def __str__(self) -> str: return "[P: {}, S: {}]".format(self.position, self.size)

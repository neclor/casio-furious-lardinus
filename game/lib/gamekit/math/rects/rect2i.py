from gamekit.math.vectors.vector2i import Vector2i

TYPE_CHECKING = False

if TYPE_CHECKING:
    from gamekit.math.vectors.vector2 import Vector2
    from gamekit.math.rects.rect2 import Rect2


class Rect2i:
    __slots__ = ("position", "size")

    position: Vector2i
    size: Vector2i

    SIDE_LEFT: int = 0
    SIDE_TOP: int = 1
    SIDE_RIGHT: int = 2
    SIDE_BOTTOM: int = 3

    def __init__(
        self,
        x: "Rect2i | Rect2 | Vector2i | Vector2 | tuple[int, int] | list[int] | int" = 0,
        y: "Vector2i | Vector2 | tuple[int, int] | list[int] | int" = 0,
        width: int = 0,
        height: int = 0,
    ) -> None: self.set(x, y, width, height)

    def set(
        self,
        x: "Rect2i | Rect2 | Vector2i | Vector2 | tuple[int, int] | list[int] | int" = 0,
        y: "Vector2i | Vector2 | tuple[int, int] | list[int] | int" = 0,
        width: int = 0,
        height: int = 0,
    ) -> "Rect2i":
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

    def copy(self) -> "Rect2i": return Rect2i(self.position.x, self.position.y, self.size.x, self.size.y)

    @property
    def end(self) -> Vector2i: return self.position + self.size

    @end.setter
    def end(self, value: Vector2i) -> None: self.size = Vector2i(value.x - self.position.x, value.y - self.position.y)

    def abs(self) -> "Rect2i":
        return Rect2i(self.position.x + min(self.size.x, 0),
                      self.position.y + min(self.size.y, 0),
                      abs(self.size.x), abs(self.size.y))

    def encloses(self, b: "Rect2i") -> bool:
        return (b.position.x >= self.position.x
                and b.position.y >= self.position.y
                and b.position.x + b.size.x <= self.position.x + self.size.x
                and b.position.y + b.size.y <= self.position.y + self.size.y)

    def expand(self, to: Vector2i) -> "Rect2i":
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
        return Rect2i(begin_x, begin_y, end_x - begin_x, end_y - begin_y)

    def get_area(self) -> int: return self.size.x * self.size.y

    def get_center(self) -> Vector2i: return self.position + self.size / 2

    def grow(self, amount: int) -> "Rect2i": return Rect2i(self.position.x - amount, self.position.y - amount, self.size.x + amount * 2, self.size.y + amount * 2)

    def grow_individual(self, left: int, top: int, right: int, bottom: int) -> "Rect2i": return Rect2i(self.position.x - left, self.position.y - top, self.size.x + left + right, self.size.y + top + bottom)

    def grow_side(self, side: int, amount: int) -> "Rect2i":
        return self.grow_individual(
            amount if side == Rect2i.SIDE_LEFT else 0,
            amount if side == Rect2i.SIDE_TOP else 0,
            amount if side == Rect2i.SIDE_RIGHT else 0,
            amount if side == Rect2i.SIDE_BOTTOM else 0)

    def has_area(self) -> bool: return self.size.x > 0 and self.size.y > 0

    def has_point(self, point: Vector2i) -> bool:
        if point.x < self.position.x:
            return False
        if point.y < self.position.y:
            return False
        if point.x >= self.position.x + self.size.x:
            return False
        if point.y >= self.position.y + self.size.y:
            return False
        return True

    def intersection(self, b: "Rect2i") -> "Rect2i":
        if not self.intersects(b):
            return Rect2i()
        pos_x = max(b.position.x, self.position.x)
        pos_y = max(b.position.y, self.position.y)
        b_end_x = b.position.x + b.size.x
        b_end_y = b.position.y + b.size.y
        end_x = self.position.x + self.size.x
        end_y = self.position.y + self.size.y
        return Rect2i(pos_x, pos_y, min(b_end_x, end_x) - pos_x, min(b_end_y, end_y) - pos_y)

    def intersects(self, b: "Rect2i") -> bool:
        if self.position.x >= b.position.x + b.size.x:
            return False
        if self.position.x + self.size.x <= b.position.x:
            return False
        if self.position.y >= b.position.y + b.size.y:
            return False
        if self.position.y + self.size.y <= b.position.y:
            return False
        return True

    def merge(self, b: "Rect2i") -> "Rect2i":
        pos_x = min(b.position.x, self.position.x)
        pos_y = min(b.position.y, self.position.y)
        end_x = max(b.position.x + b.size.x, self.position.x + self.size.x)
        end_y = max(b.position.y + b.size.y, self.position.y + self.size.y)
        return Rect2i(pos_x, pos_y, end_x - pos_x, end_y - pos_y)

    def __eq__(self, o: object) -> bool: return isinstance(o, Rect2i) and self.position == o.position and self.size == o.size

    def __ne__(self, o: object) -> bool: return not (isinstance(o, Rect2i) and self.position == o.position and self.size == o.size)

    def __hash__(self) -> int: return hash((self.position.x, self.position.y, self.size.x, self.size.y))

    def __repr__(self) -> str: return "Rect2i({}, {}, {}, {})".format(self.position.x, self.position.y, self.size.x, self.size.y)

    def __str__(self) -> str: return "[P: {}, S: {}]".format(self.position, self.size)

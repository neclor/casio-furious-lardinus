from gamekit.math.vectors.vector2 import Vector2
from gamekit.math.rects.rect2i import Rect2i

TYPE_CHECKING = False

if TYPE_CHECKING:
    from gamekit.math.vectors.vector2i import Vector2i


class Rect2:
    __slots__ = ("position", "size")

    position: Vector2
    size: Vector2

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

    def __eq__(self, o: object) -> bool: return isinstance(o, Rect2) and self.position == o.position and self.size == o.size

    def __ne__(self, o: object) -> bool: return not (isinstance(o, Rect2) and self.position == o.position and self.size == o.size)

    def __hash__(self) -> int: return hash((self.position.x, self.position.y, self.size.x, self.size.y))

    def __repr__(self) -> str: return "Rect2({}, {}, {}, {})".format(self.position.x, self.position.y, self.size.x, self.size.y)

    def __str__(self) -> str: return "[P: {}, S: {}]".format(self.position, self.size)

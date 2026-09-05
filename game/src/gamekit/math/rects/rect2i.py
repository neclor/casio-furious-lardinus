from gamekit.math.vectors.vector2i import Vector2i

TYPE_CHECKING = False

if TYPE_CHECKING:
    from gamekit.math.vectors.vector2 import Vector2
    from gamekit.math.rects.rect2 import Rect2


class Rect2i:
    __slots__ = ("position", "size")

    position: Vector2i
    size: Vector2i

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

    def __eq__(self, o: object) -> bool: return isinstance(o, Rect2i) and self.position == o.position and self.size == o.size

    def __ne__(self, o: object) -> bool: return not (isinstance(o, Rect2i) and self.position == o.position and self.size == o.size)

    def __hash__(self) -> int: return hash((self.position.x, self.position.y, self.size.x, self.size.y))

    def __repr__(self) -> str: return "Rect2i({}, {}, {}, {})".format(self.position.x, self.position.y, self.size.x, self.size.y)

    def __str__(self) -> str: return "[P: {}, S: {}]".format(self.position, self.size)

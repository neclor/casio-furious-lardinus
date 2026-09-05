TYPE_CHECKING = False

if TYPE_CHECKING:
    from gamekit.math.vectors.vector2i import Vector2i


class Font:
    __slots__ = ()

    @property
    def height(self) -> int: raise NotImplementedError

    def measure(self, text: str) -> "Vector2i": raise NotImplementedError

    def dispose(self) -> None: raise NotImplementedError

TYPE_CHECKING = False

if TYPE_CHECKING:
    from gamekit.math.vectors.vector2i import Vector2i


class Texture:
    __slots__ = ()

    @property
    def width(self) -> int: raise NotImplementedError

    @property
    def height(self) -> int: raise NotImplementedError

    @property
    def size(self) -> "Vector2i": raise NotImplementedError

    def dispose(self) -> None: raise NotImplementedError

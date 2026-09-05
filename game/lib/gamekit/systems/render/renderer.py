TYPE_CHECKING = False

if TYPE_CHECKING:
    from gamekit.math.rects.rect2 import Rect2
    from gamekit.math.rects.rect2i import Rect2i
    from gamekit.math.vectors.vector2 import Vector2
    from gamekit.math.vectors.vector2i import Vector2i
    from gamekit.systems.render.color import Color
    from gamekit.systems.render.font import Font
    from gamekit.systems.render.texture import Texture


class Renderer:
    __slots__ = ()

    @property
    def size(self) -> "Vector2i": raise NotImplementedError

    def load_texture(self, path: str) -> "Texture": raise NotImplementedError

    def load_font(self, path: str, size: int) -> "Font": raise NotImplementedError

    def clear(self, color: "Color") -> None: raise NotImplementedError

    def set_pixel(self, pos: "Vector2i", color: "Color", z: int = 0) -> None: raise NotImplementedError

    def draw_line(self, start: "Vector2", end: "Vector2", color: "Color", width: float = 1.0, z: int = 0) -> None: raise NotImplementedError

    def draw_rect(self, rect: "Rect2", color: "Color", z: int = 0) -> None: raise NotImplementedError

    def draw_text(self, font: "Font", text: str, position: "Vector2", color: "Color", z: int = 0) -> None: raise NotImplementedError

    def draw_texture(
        self,
        source: "Texture",
        destination: "Rect2",
        src: "Rect2i | None" = None,
        z: int = 0,
        flip_h: bool = False,
        flip_v: bool = False,
        tint: "Color | None" = None,
    ) -> None: raise NotImplementedError

    def update_screen(self) -> None: raise NotImplementedError

    def toggle_fullscreen(self) -> None: raise NotImplementedError

    def shutdown(self) -> None: raise NotImplementedError

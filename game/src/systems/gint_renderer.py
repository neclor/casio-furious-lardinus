import gint

from gamekit.systems.render.renderer import Renderer
from gamekit.systems.render.texture import Texture
from gamekit.systems.render.font import Font
from gamekit.math.vectors.vector2i import Vector2i

TYPE_CHECKING = False

if TYPE_CHECKING:
    from typing import Callable
    from gamekit.math.rects.rect2 import Rect2
    from gamekit.math.rects.rect2i import Rect2i
    from gamekit.math.vectors.vector2 import Vector2
    from gamekit.systems.render.color import Color

    _RenderCommand = tuple[int, Callable[..., None], tuple]


_IS_MONO: bool = gint.DWIDTH <= 128


def _to_gint_color(color: "Color") -> int:
    if _IS_MONO:
        luminance = (color.r * 299 + color.g * 587 + color.b * 114) // 1000
        if luminance < 64:
            return gint.C_BLACK
        if luminance < 128:
            return gint.C_DARK
        if luminance < 192:
            return gint.C_LIGHT
        return gint.C_WHITE
    return gint.C_RGB(color.r >> 3, color.g >> 3, color.b >> 3)


def _to_module_name(path: str) -> str:
    if path.startswith("src/"):
        path = path[4:]
    if path.endswith(".png"):
        path = path[:-4]
    return path.replace("/", ".")


class GintTexture(Texture):
    __slots__ = ("image",)

    image: gint.image

    def __init__(self, image: gint.image) -> None:
        self.image = image

    @property
    def width(self) -> int: return self.image.width

    @property
    def height(self) -> int: return self.image.height

    @property
    def size(self) -> Vector2i: return Vector2i(self.image.width, self.image.height)

    def dispose(self) -> None:
        pass


class GintFont(Font):
    __slots__ = ("font", "_height", "_char_width", "_widths")

    font: gint.font
    _height: int
    _char_width: int
    _widths: "bytes | None"

    def __init__(self, font: gint.font, height: int, char_width: int, widths: "bytes | None") -> None:
        self.font = font
        self._height = height
        self._char_width = char_width
        self._widths = widths

    @property
    def height(self) -> int: return self._height

    def measure(self, text: str) -> Vector2i:
        width = 0
        for character in text:
            width += self._glyph_width(character)
        return Vector2i(width, self._height)

    def _glyph_width(self, character: str) -> int:
        if self._widths is None:
            return self._char_width
        index = ord(character) - 0x20
        if 0 <= index < len(self._widths):
            return self._widths[index]
        return self._char_width

    def dispose(self) -> None:
        pass


class GintRenderer(Renderer):
    __slots__ = ("_commands", "_textures")

    _commands: "list[_RenderCommand]"
    _textures: "dict[str, Texture]"

    def __init__(self) -> None:
        self._commands = []
        self._textures = {}

    @property
    def size(self) -> Vector2i: return Vector2i(gint.DWIDTH, gint.DHEIGHT)

    def load_texture(self, path: str) -> Texture:
        texture = self._textures.get(path)
        if texture is None:
            module = __import__(_to_module_name(path), None, None, ("image",), 0)
            texture = GintTexture(module.image)
            self._textures[path] = texture
        return texture

    def load_font(self, path: str, size: int) -> Font:
        # No OTF -> gint.font conversion pipeline exists yet (unlike sprites, which
        # go through tools/build_gint_textures.py), so fall back to gint's builtin
        # font: dfont(None) resets to it, and these are its approximate metrics.
        return GintFont(None, height=7, char_width=5, widths=None)

    def clear(self, color: "Color") -> None: gint.dclear(_to_gint_color(color))

    def set_pixel(self, pos: "Vector2i", color: "Color", z: int = 0) -> None: self._commands.append((z, self._blit_pixel, (int(pos.x), int(pos.y), color)))

    def draw_line(self, start: "Vector2", end: "Vector2", color: "Color", width: float = 1.0, z: int = 0) -> None: self._commands.append((z, self._blit_line, (start, end, color)))

    def draw_rect(self, rect: "Rect2", color: "Color", z: int = 0) -> None: self._commands.append((z, self._blit_rect, (rect, color)))

    def draw_text(self, font: Font, text: str, position: "Vector2", color: "Color", z: int = 0) -> None: self._commands.append((z, self._blit_text, (font, text, position, color)))

    def draw_texture(
        self,
        source: Texture,
        destination: "Rect2",
        src: "Rect2i | None" = None,
        z: int = 0,
        flip_h: bool = False,
        flip_v: bool = False,
        tint: "Color | None" = None,
    ) -> None:
        if tint is not None: raise NotImplementedError
        self._commands.append((z, self._blit_texture, (source, destination, src, flip_h, flip_v)))

    def update_screen(self) -> None:
        self._commands.sort(key=lambda command: command[0])
        for _, blit, args in self._commands:
            blit(*args)
        self._commands = []
        gint.dupdate()

    def toggle_fullscreen(self) -> None:
        pass

    def shutdown(self) -> None:
        if _IS_MONO:
            gint.dgray(gint.DGRAY_OFF)

    def _blit_pixel(self, x: int, y: int, color: "Color") -> None: gint.dpixel(x, y, _to_gint_color(color))

    def _blit_line(self, start: "Vector2", end: "Vector2", color: "Color") -> None: gint.dline(int(start.x), int(start.y), int(end.x), int(end.y), _to_gint_color(color))

    def _blit_rect(self, rect: "Rect2", color: "Color") -> None:
        gint.drect(
            int(rect.position.x),
            int(rect.position.y),
            int(rect.position.x + rect.size.x) - 1,
            int(rect.position.y + rect.size.y) - 1,
            _to_gint_color(color),
        )

    def _blit_text(self, font: GintFont, text: str, position: "Vector2", color: "Color") -> None:
        gint.dfont(font.font)
        gint.dtext(int(position.x), int(position.y), _to_gint_color(color), text)

    def _blit_texture(
        self,
        source: GintTexture,
        destination: "Rect2",
        src: "Rect2i | None",
        flip_h: bool,
        flip_v: bool,
    ) -> None:
        image = source.image
        data = image.data
        word_width = (image.width + 31) // 32

        if src is not None:
            src_x = int(src.position.x)
            src_y = int(src.position.y)
            src_w = int(src.size.x)
            src_h = int(src.size.y)
        else:
            src_x = 0
            src_y = 0
            src_w = image.width
            src_h = image.height

        dest_x = int(destination.position.x)
        dest_y = int(destination.position.y)
        dest_w = int(destination.size.x)
        dest_h = int(destination.size.y)
        if dest_w <= 0 or dest_h <= 0 or src_w <= 0 or src_h <= 0: return

        source_x_by_column = [0] * dest_w
        for dx in range(dest_w):
            offset = (dx * src_w) // dest_w
            source_x_by_column[dx] = src_x + (src_w - 1 - offset if flip_h else offset)

        source_y_by_row = [0] * dest_h
        for dy in range(dest_h):
            offset = (dy * src_h) // dest_h
            source_y_by_row[dy] = src_y + (src_h - 1 - offset if flip_v else offset)

        dpixel = gint.dpixel
        c_black = gint.C_BLACK
        c_dark = gint.C_DARK
        c_light = gint.C_LIGHT
        c_white = gint.C_WHITE

        cached_source_x = None
        cached_column: "list[tuple[int, int]]" = []

        for column, source_x in enumerate(source_x_by_column):
            screen_x = dest_x + column
            if source_x != cached_source_x:
                cached_column = []
                word_col = source_x >> 5
                byte_in_word = (source_x >> 3) & 3
                bit = ~source_x & 7
                for row, source_y in enumerate(source_y_by_row):
                    base = (source_y * word_width + word_col) * 12 + byte_in_word
                    if not (data[base] >> bit) & 1:
                        continue
                    black_or_light = (data[base + 4] >> bit) & 1
                    black_or_dark = (data[base + 8] >> bit) & 1
                    color = (
                        c_black if (black_or_light and black_or_dark)
                        else c_dark if black_or_dark
                        else c_light if black_or_light
                        else c_white
                    )
                    cached_column.append((row, color))
                cached_source_x = source_x

            for row, color in cached_column:
                dpixel(screen_x, dest_y + row, color)


def create_renderer() -> GintRenderer:
    if _IS_MONO:
        gint.dgray(gint.DGRAY_ON)
    return GintRenderer()

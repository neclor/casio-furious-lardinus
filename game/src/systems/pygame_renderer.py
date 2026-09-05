from typing import TYPE_CHECKING, Callable

import pygame

from gamekit.systems.render.renderer import Renderer
from gamekit.systems.render.texture import Texture
from gamekit.systems.render.font import Font
from gamekit.math.vectors.vector2i import Vector2i

if TYPE_CHECKING:
    from gamekit.math.rects.rect2 import Rect2
    from gamekit.math.rects.rect2i import Rect2i
    from gamekit.math.vectors.vector2 import Vector2
    from gamekit.systems.render.color import Color


_RenderCommand = tuple[int, Callable[..., None], tuple]


class PygameTexture(Texture):
    __slots__ = ("surface",)

    surface: pygame.Surface

    def __init__(self, surface: pygame.Surface) -> None:
        self.surface = surface

    @property
    def width(self) -> int: return self.surface.get_width()

    @property
    def height(self) -> int: return self.surface.get_height()

    @property
    def size(self) -> Vector2i: return Vector2i(self.surface.get_width(), self.surface.get_height())

    def dispose(self) -> None: pass


class PygameFont(Font):
    __slots__ = ("font",)

    font: pygame.font.Font

    def __init__(self, font: pygame.font.Font) -> None:
        self.font = font

    @property
    def height(self) -> int: return self.font.get_height()

    def measure(self, text: str) -> Vector2i:
        w, h = self.font.size(text)
        return Vector2i(w, h)

    def dispose(self) -> None: pass


class PygameRenderer(Renderer):
    __slots__ = ("_surface", "_commands")

    _surface: pygame.Surface
    _commands: list[_RenderCommand]

    def __init__(self, surface: pygame.Surface) -> None:
        self._surface = surface
        self._commands = []

    @property
    def size(self) -> Vector2i:
        return Vector2i(self._surface.get_width(), self._surface.get_height())

    def load_texture(self, path: str) -> Texture:
        return PygameTexture(pygame.image.load(path).convert_alpha())

    def load_font(self, path: str, size: int) -> Font:
        return PygameFont(pygame.font.Font(path, size))

    def clear(self, color: "Color") -> None:
        self._surface.fill((color.r, color.g, color.b))

    def set_pixel(self, pos: "Vector2i", color: "Color", z: int = 0) -> None:
        self._commands.append((z, self._blit_pixel, (int(pos.x), int(pos.y), color)))

    def draw_line(self, start: "Vector2", end: "Vector2", color: "Color", width: float = 1.0, z: int = 0) -> None:
        self._commands.append((z, self._blit_line, (start, end, color, max(1, int(width)))))

    def draw_rect(self, rect: "Rect2", color: "Color", z: int = 0) -> None:
        self._commands.append((z, self._blit_rect, (rect, color)))

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
        self._commands.append((z, self._blit_texture, (source, destination, src, flip_h, flip_v, tint)))

    def draw_text(self, font: Font, text: str, position: "Vector2", color: "Color", z: int = 0) -> None:
        self._commands.append((z, self._blit_text, (font, text, position, color)))

    def update_screen(self) -> None:
        self._commands.sort(key=lambda command: command[0])
        for _, blit, args in self._commands:
            blit(*args)
        self._commands = []
        pygame.display.flip()

    def toggle_fullscreen(self) -> None:
        pygame.display.toggle_fullscreen()

    def shutdown(self) -> None:
        pygame.quit()

    def _blit_pixel(self, x: int, y: int, color: "Color") -> None:
        self._surface.set_at((x, y), (color.r, color.g, color.b, color.a))

    def _blit_line(self, start: "Vector2", end: "Vector2", color: "Color", width: int) -> None:
        pygame.draw.line(self._surface, (color.r, color.g, color.b),
                         (start.x, start.y), (end.x, end.y), width)

    def _blit_rect(self, rect: "Rect2", color: "Color") -> None:
        pygame.draw.rect(self._surface, (color.r, color.g, color.b),
                         pygame.Rect(rect.position.x, rect.position.y, rect.size.x, rect.size.y))

    def _blit_texture(
        self,
        source: PygameTexture,
        destination: "Rect2",
        src: "Rect2i | None",
        flip_h: bool,
        flip_v: bool,
        tint: "Color | None",
    ) -> None:
        surface: pygame.Surface = source.surface
        if src is not None:
            surface = surface.subsurface(
                pygame.Rect(src.position.x, src.position.y, src.size.x, src.size.y)
            )
        target_size = (int(destination.size.x), int(destination.size.y))
        if target_size != surface.get_size():
            surface = pygame.transform.scale(surface, target_size)
        if flip_h or flip_v:
            surface = pygame.transform.flip(surface, flip_h, flip_v)
        if tint is not None:
            surface = surface.copy()
            surface.fill((tint.r, tint.g, tint.b, tint.a), special_flags=pygame.BLEND_RGBA_MULT)
        self._surface.blit(surface, (int(destination.position.x), int(destination.position.y)))

    def _blit_text(self, font: PygameFont, text: str, position: "Vector2", color: "Color") -> None:
        image: pygame.Surface = font.font.render(text, True, (color.r, color.g, color.b))
        self._surface.blit(image, (int(position.x), int(position.y)))


def create_renderer(title: str, size: "tuple[int, int]") -> PygameRenderer:
    pygame.init()
    pygame.display.set_mode(size, pygame.SCALED)
    pygame.display.set_caption(title)
    return PygameRenderer(pygame.display.get_surface())

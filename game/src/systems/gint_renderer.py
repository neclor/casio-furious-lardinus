import sys
import gint
from gamekit.math.vectors.vector2i import Vector2i
_IS_MONO = gint.DWIDTH <= 128
_commands = []
_textures = {}

def _to_gint_color(color):
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

def _to_module_name(path):
    if path.startswith('src/'):
        path = path[4:]
    if path.endswith('.png'):
        path = path[:-4]
    return path.replace('/', '.')

class GintTexture:
    __slots__ = ('image',)

    def __init__(self, image):
        self.image = image

    @property
    def width(self):
        return self.image.width

    @property
    def height(self):
        return self.image.height

    @property
    def size(self):
        return Vector2i(self.image.width, self.image.height)

    def dispose(self):
        pass

class GintFont:
    __slots__ = ('font', '_height', '_char_width', '_widths')

    def __init__(self, font, height, char_width, widths):
        self.font = font
        self._height = height
        self._char_width = char_width
        self._widths = widths

    @property
    def height(self):
        return self._height

    def measure(self, text):
        width = 0
        for character in text:
            width += self._glyph_width(character)
        return Vector2i(width, self._height)

    def _glyph_width(self, character):
        if self._widths is None:
            return self._char_width
        index = ord(character) - 32
        if 0 <= index < len(self._widths):
            return self._widths[index]
        return self._char_width

    def dispose(self):
        pass

def load_texture(path):
    texture = _textures.get(path)
    if texture is None:
        module = __import__(_to_module_name(path), None, None, ('image',), 0)
        texture = GintTexture(module.image)
        _textures[path] = texture
    return texture

def load_font(path, size):
    return GintFont(None, height=7, char_width=5, widths=None)

def clear(color):
    gint.dclear(_to_gint_color(color))

def draw_rect(rect, color, z=0):
    _commands.append((z, _blit_rect, (rect, color)))

def draw_text(font, text, position, color, z=0):
    _commands.append((z, _blit_text, (font, text, position, color)))

def draw_texture(source, destination, src=None, z=0, flip_h=False, flip_v=False, tint=None):
    if tint is not None:
        raise NotImplementedError
    _commands.append((z, _blit_texture, (source, destination, src, flip_h, flip_v)))

def update_screen():
    global _commands
    _commands.sort(key=lambda command: command[0])
    for _, blit, args in _commands:
        blit(*args)
    _commands = []
    gint.dupdate()

def toggle_fullscreen():
    pass

def shutdown():
    if _IS_MONO:
        gint.dgray(gint.DGRAY_OFF)

def _blit_rect(rect, color):
    gint.drect(int(rect.position.x), int(rect.position.y), int(rect.position.x + rect.size.x) - 1, int(rect.position.y + rect.size.y) - 1, _to_gint_color(color))

def _blit_text(font, text, position, color):
    gint.dfont(font.font)
    gint.dtext(int(position.x), int(position.y), _to_gint_color(color), text)

def _blit_texture(source, destination, src, flip_h, flip_v):
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
    if dest_w <= 0 or dest_h <= 0 or src_w <= 0 or (src_h <= 0):
        return
    source_x_by_column = [0] * dest_w
    for dx in range(dest_w):
        offset = dx * src_w // dest_w
        source_x_by_column[dx] = src_x + (src_w - 1 - offset if flip_h else offset)
    source_y_by_row = [0] * dest_h
    for dy in range(dest_h):
        offset = dy * src_h // dest_h
        source_y_by_row[dy] = src_y + (src_h - 1 - offset if flip_v else offset)
    dpixel = gint.dpixel
    c_black = gint.C_BLACK
    c_dark = gint.C_DARK
    c_light = gint.C_LIGHT
    c_white = gint.C_WHITE
    cached_source_x = None
    cached_column = []
    for column, source_x in enumerate(source_x_by_column):
        screen_x = dest_x + column
        if source_x != cached_source_x:
            cached_column = []
            word_col = source_x >> 5
            byte_in_word = source_x >> 3 & 3
            bit = ~source_x & 7
            for row, source_y in enumerate(source_y_by_row):
                base = (source_y * word_width + word_col) * 12 + byte_in_word
                if not data[base] >> bit & 1:
                    continue
                black_or_light = data[base + 4] >> bit & 1
                black_or_dark = data[base + 8] >> bit & 1
                color = c_black if black_or_light and black_or_dark else c_dark if black_or_dark else c_light if black_or_light else c_white
                cached_column.append((row, color))
            cached_source_x = source_x
        for row, color in cached_column:
            dpixel(screen_x, dest_y + row, color)

def create_renderer():
    if _IS_MONO:
        gint.dgray(gint.DGRAY_ON)
    return sys.modules[__name__]

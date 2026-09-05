DWIDTH: int
DHEIGHT: int

C_BLACK: int
C_DARK: int
C_LIGHT: int
C_WHITE: int

def C_RGB(r: int, g: int, b: int) -> int: ...

def dclear(color: int) -> None: ...
def dpixel(x: int, y: int, color: int) -> None: ...
def dline(x1: int, y1: int, x2: int, y2: int, color: int) -> None: ...
def drect(x1: int, y1: int, x2: int, y2: int, color: int) -> None: ...
def dupdate() -> None: ...

DGRAY_ON: int
DGRAY_OFF: int

def dgray(mode: int) -> None: ...
def dgray_enabled() -> bool: ...

IMAGE_MONO: int
IMAGE_MONO_ALPHA: int
IMAGE_GRAY: int
IMAGE_GRAY_ALPHA: int
IMAGE_P8_RGB565: int
IMAGE_RGB565: int
IMAGE_RGB565A: int

class image:
    format: int
    width: int
    height: int
    data: bytes

    def __init__(self, format: int, width: int, height: int, data: bytes) -> None: ...

def image_rgb565a(width: int, height: int, data: bytes, alpha: bytes) -> image: ...
def dimage(x: int, y: int, img: image) -> None: ...
def dsubimage(x: int, y: int, img: image, sx: int, sy: int, sw: int, sh: int) -> None: ...

class font:
    def __init__(
        self,
        proportional: int,
        line_height: int,
        char_width: int,
        char_spacing: int,
        glyph_count: int,
        block_count: int,
        block_size: int,
        index: bytes,
        data: bytes,
    ) -> None: ...

def dfont(font: font | None) -> None: ...
def dtext(x: int, y: int, color: int, text: str) -> None: ...
def dtext_opt(x: int, y: int, fg: int, bg: int, halign: int, valign: int, text: str, maxwidth: int) -> None: ...

KEYEV_NONE: int
KEYEV_DOWN: int
KEYEV_UP: int
KEYEV_HOLD: int

class KeyEvent:
    type: int
    key: int
    time: int

def pollevent() -> KeyEvent: ...

KEY_LEFT: int
KEY_RIGHT: int
KEY_UP: int
KEY_DOWN: int
KEY_EXE: int
KEY_EXIT: int
KEY_DEL: int
KEY_ACON: int
KEY_SHIFT: int
KEY_0: int
KEY_1: int
KEY_2: int
KEY_3: int
KEY_4: int
KEY_5: int
KEY_6: int
KEY_7: int
KEY_8: int
KEY_9: int
KEY_F1: int
KEY_F2: int
KEY_F3: int
KEY_F4: int
KEY_F5: int
KEY_F6: int

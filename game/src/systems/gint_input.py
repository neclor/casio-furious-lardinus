import gint

from gamekit.systems.input import Input, Key
from gamekit.math.vectors.vector2 import Vector2


_KEY_MAP: dict[int, int] = {
    Key.LEFT: gint.KEY_LEFT,
    Key.RIGHT: gint.KEY_RIGHT,
    Key.UP: gint.KEY_UP,
    Key.DOWN: gint.KEY_DOWN,
    Key.ENTER: gint.KEY_EXE,
    Key.ESCAPE: gint.KEY_EXIT,
    Key.DELETE: gint.KEY_DEL,
    Key.AC: gint.KEY_ACON,
    Key.LSHIFT: gint.KEY_SHIFT,
    Key.NUM_0: gint.KEY_0,
    Key.NUM_1: gint.KEY_1,
    Key.NUM_2: gint.KEY_2,
    Key.NUM_3: gint.KEY_3,
    Key.NUM_4: gint.KEY_4,
    Key.NUM_5: gint.KEY_5,
    Key.NUM_6: gint.KEY_6,
    Key.NUM_7: gint.KEY_7,
    Key.NUM_8: gint.KEY_8,
    Key.NUM_9: gint.KEY_9,
    Key.F1: gint.KEY_F1,
    Key.F2: gint.KEY_F2,
    Key.F3: gint.KEY_F3,
    Key.F4: gint.KEY_F4,
    Key.F5: gint.KEY_F5,
    Key.F6: gint.KEY_F6,
}

_NATIVE_TO_KEY: dict[int, int] = {native: key for key, native in _KEY_MAP.items()}


class GintInput(Input):
    __slots__ = ("_down", "_pressed_this_frame", "_released_this_frame")

    _down: set[int]
    _pressed_this_frame: set[int]
    _released_this_frame: set[int]

    def __init__(self) -> None:
        self._down = set()
        self._pressed_this_frame = set()
        self._released_this_frame = set()

    def poll(self) -> None:
        self._pressed_this_frame = set()
        self._released_this_frame = set()
        while True:
            event = gint.pollevent()
            if event.type == gint.KEYEV_NONE:
                break
            key = _NATIVE_TO_KEY.get(event.key)
            if key is None:
                continue
            if event.type == gint.KEYEV_DOWN:
                self._down.add(key)
                self._pressed_this_frame.add(key)
            elif event.type == gint.KEYEV_UP:
                self._down.discard(key)
                self._released_this_frame.add(key)

    def is_key_down(self, key: int) -> bool:
        return key in self._down

    def is_key_pressed(self, key: int) -> bool:
        return key in self._pressed_this_frame

    def is_key_released(self, key: int) -> bool:
        return key in self._released_this_frame

    def pressed_keys(self) -> list[int]:
        return list(self._pressed_this_frame)

    def axis(self, negative: int, positive: int) -> float:
        return (1.0 if positive in self._down else 0.0) - (1.0 if negative in self._down else 0.0)

    def mouse_position(self) -> Vector2:
        return Vector2()

    def mouse_delta(self) -> Vector2:
        return Vector2()

    def wheel(self) -> float:
        return 0.0

    def is_mouse_down(self, button: int) -> bool:
        return False

    def is_mouse_pressed(self, button: int) -> bool:
        return False

    def is_mouse_released(self, button: int) -> bool:
        return False

    def set_mouse_captured(self, captured: bool) -> None:
        pass

    def is_mouse_captured(self) -> bool:
        return False

    def should_quit(self) -> bool:
        return False

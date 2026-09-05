TYPE_CHECKING = False

if TYPE_CHECKING:
    from gamekit.math.vectors.vector2 import Vector2


class Key:
    UNKNOWN: int = 0

    A: int = 1
    B: int = 2
    C: int = 3
    D: int = 4
    E: int = 5
    F: int = 6
    G: int = 7
    H: int = 8
    I: int = 9
    J: int = 10
    K: int = 11
    L: int = 12
    M: int = 13
    N: int = 14
    O: int = 15
    P: int = 16
    Q: int = 17
    R: int = 18
    S: int = 19
    T: int = 20
    U: int = 21
    V: int = 22
    W: int = 23
    X: int = 24
    Y: int = 25
    Z: int = 26

    NUM_0: int = 30
    NUM_1: int = 31
    NUM_2: int = 32
    NUM_3: int = 33
    NUM_4: int = 34
    NUM_5: int = 35
    NUM_6: int = 36
    NUM_7: int = 37
    NUM_8: int = 38
    NUM_9: int = 39

    SPACE: int = 50
    ENTER: int = 51
    ESCAPE: int = 52
    TAB: int = 53
    BACKSPACE: int = 54
    DELETE: int = 55
    AC: int = 56

    LEFT: int = 60
    RIGHT: int = 61
    UP: int = 62
    DOWN: int = 63

    LSHIFT: int = 70
    RSHIFT: int = 71
    LCTRL: int = 72
    RCTRL: int = 73
    LALT: int = 74
    RALT: int = 75

    F1: int = 80
    F2: int = 81
    F3: int = 82
    F4: int = 83
    F5: int = 84
    F6: int = 85
    F7: int = 86
    F8: int = 87
    F9: int = 88
    F10: int = 89
    F11: int = 90
    F12: int = 91


class MouseButton:
    LEFT: int = 0
    MIDDLE: int = 1
    RIGHT: int = 2


class Input:
    __slots__ = ()

    def poll(self) -> None: raise NotImplementedError

    def is_key_down(self, key: int) -> bool: raise NotImplementedError

    def is_key_pressed(self, key: int) -> bool: raise NotImplementedError

    def is_key_released(self, key: int) -> bool: raise NotImplementedError

    def pressed_keys(self) -> "list[int]": raise NotImplementedError

    def axis(self, negative: int, positive: int) -> float: raise NotImplementedError

    def mouse_position(self) -> "Vector2": raise NotImplementedError

    def mouse_delta(self) -> "Vector2": raise NotImplementedError

    def wheel(self) -> float: raise NotImplementedError

    def is_mouse_down(self, button: int) -> bool: raise NotImplementedError

    def is_mouse_pressed(self, button: int) -> bool: raise NotImplementedError

    def is_mouse_released(self, button: int) -> bool: raise NotImplementedError

    def set_mouse_captured(self, captured: bool) -> None: raise NotImplementedError

    def is_mouse_captured(self) -> bool: raise NotImplementedError

    def should_quit(self) -> bool: raise NotImplementedError

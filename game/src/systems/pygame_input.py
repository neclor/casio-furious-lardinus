import pygame

from gamekit.systems.input import Input, Key, MouseButton
from gamekit.math.vectors.vector2 import Vector2


_KEY_MAP: dict[int, int] = {
    Key.A: pygame.K_a, Key.B: pygame.K_b, Key.C: pygame.K_c, Key.D: pygame.K_d,
    Key.E: pygame.K_e, Key.F: pygame.K_f, Key.G: pygame.K_g, Key.H: pygame.K_h,
    Key.I: pygame.K_i, Key.J: pygame.K_j, Key.K: pygame.K_k, Key.L: pygame.K_l,
    Key.M: pygame.K_m, Key.N: pygame.K_n, Key.O: pygame.K_o, Key.P: pygame.K_p,
    Key.Q: pygame.K_q, Key.R: pygame.K_r, Key.S: pygame.K_s, Key.T: pygame.K_t,
    Key.U: pygame.K_u, Key.V: pygame.K_v, Key.W: pygame.K_w, Key.X: pygame.K_x,
    Key.Y: pygame.K_y, Key.Z: pygame.K_z,
    Key.NUM_0: pygame.K_0, Key.NUM_1: pygame.K_1, Key.NUM_2: pygame.K_2,
    Key.NUM_3: pygame.K_3, Key.NUM_4: pygame.K_4, Key.NUM_5: pygame.K_5,
    Key.NUM_6: pygame.K_6, Key.NUM_7: pygame.K_7, Key.NUM_8: pygame.K_8,
    Key.NUM_9: pygame.K_9,
    Key.SPACE: pygame.K_SPACE, Key.ENTER: pygame.K_RETURN, Key.ESCAPE: pygame.K_ESCAPE,
    Key.TAB: pygame.K_TAB, Key.BACKSPACE: pygame.K_BACKSPACE, Key.DELETE: pygame.K_DELETE,
    Key.LEFT: pygame.K_LEFT, Key.RIGHT: pygame.K_RIGHT, Key.UP: pygame.K_UP, Key.DOWN: pygame.K_DOWN,
    Key.LSHIFT: pygame.K_LSHIFT, Key.RSHIFT: pygame.K_RSHIFT,
    Key.LCTRL: pygame.K_LCTRL, Key.RCTRL: pygame.K_RCTRL,
    Key.LALT: pygame.K_LALT, Key.RALT: pygame.K_RALT,
    Key.F1: pygame.K_F1, Key.F2: pygame.K_F2, Key.F3: pygame.K_F3, Key.F4: pygame.K_F4,
    Key.F5: pygame.K_F5, Key.F6: pygame.K_F6, Key.F7: pygame.K_F7, Key.F8: pygame.K_F8,
    Key.F9: pygame.K_F9, Key.F10: pygame.K_F10, Key.F11: pygame.K_F11, Key.F12: pygame.K_F12,
}

_BUTTON_INDEX: dict[int, int] = {
    MouseButton.LEFT: 0,
    MouseButton.MIDDLE: 1,
    MouseButton.RIGHT: 2,
}


class PygameInput(Input):
    __slots__ = (
        "_down", "_prev_down", "_pressed_this_frame",
        "_mouse", "_prev_mouse", "_mouse_pos", "_mouse_rel", "_wheel", "_captured", "_quit",
    )

    _down: set[int]
    _prev_down: set[int]
    _pressed_this_frame: list[int]
    _mouse: tuple
    _prev_mouse: tuple
    _mouse_pos: tuple[int, int]
    _mouse_rel: tuple[int, int]
    _wheel: float
    _captured: bool
    _quit: bool

    def __init__(self) -> None:
        self._down = set()
        self._prev_down = set()
        self._pressed_this_frame = []
        self._mouse = (False, False, False)
        self._prev_mouse = (False, False, False)
        self._mouse_pos = (0, 0)
        self._mouse_rel = (0, 0)
        self._wheel = 0.0
        self._captured = False
        self._quit = False

    def poll(self) -> None:
        self._wheel = 0.0
        self._quit = False
        event: pygame.event.Event
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                self._wheel += event.y
            elif event.type == pygame.QUIT:
                self._quit = True

        self._prev_down = self._down
        held = pygame.key.get_pressed()
        self._down = {key for key, native in _KEY_MAP.items() if held[native]}
        self._pressed_this_frame = [key for key in self._down if key not in self._prev_down]

        self._prev_mouse = self._mouse
        self._mouse = pygame.mouse.get_pressed()
        self._mouse_pos = pygame.mouse.get_pos()
        self._mouse_rel = pygame.mouse.get_rel()

    def is_key_down(self, key: int) -> bool:
        return key in self._down

    def is_key_pressed(self, key: int) -> bool:
        return key in self._down and key not in self._prev_down

    def is_key_released(self, key: int) -> bool:
        return key not in self._down and key in self._prev_down

    def pressed_keys(self) -> list[int]:
        return list(self._pressed_this_frame)

    def axis(self, negative: int, positive: int) -> float:
        return (1.0 if positive in self._down else 0.0) - (1.0 if negative in self._down else 0.0)

    def mouse_position(self) -> Vector2:
        return Vector2(self._mouse_pos[0], self._mouse_pos[1])

    def mouse_delta(self) -> Vector2:
        return Vector2(self._mouse_rel[0], self._mouse_rel[1])

    def wheel(self) -> float:
        return self._wheel

    def is_mouse_down(self, button: int) -> bool:
        return bool(self._mouse[_BUTTON_INDEX[button]])

    def is_mouse_pressed(self, button: int) -> bool:
        index = _BUTTON_INDEX[button]
        return bool(self._mouse[index]) and not self._prev_mouse[index]

    def is_mouse_released(self, button: int) -> bool:
        index = _BUTTON_INDEX[button]
        return not self._mouse[index] and bool(self._prev_mouse[index])

    def set_mouse_captured(self, captured: bool) -> None:
        pygame.mouse.set_visible(not captured)
        pygame.event.set_grab(captured)
        self._captured = captured

    def is_mouse_captured(self) -> bool:
        return self._captured

    def should_quit(self) -> bool:
        return self._quit

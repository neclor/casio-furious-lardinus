TYPE_CHECKING = False

if TYPE_CHECKING:
    from gamekit.systems.input import Input


class Action:
    __slots__ = ("_keys", "_mouse_buttons")

    def __init__(self) -> None:
        self._keys: "list[int]" = []
        self._mouse_buttons: "list[int]" = []

    def bind_key(self, key: int) -> "Action":
        self._keys.append(key)
        return self

    def bind_mouse_button(self, button: int) -> "Action":
        self._mouse_buttons.append(button)
        return self

    def is_down(self, input: "Input") -> bool:
        for key in self._keys:
            if input.is_key_down(key):
                return True
        for button in self._mouse_buttons:
            if input.is_mouse_down(button):
                return True
        return False

    def is_pressed(self, input: "Input") -> bool:
        for key in self._keys:
            if input.is_key_pressed(key):
                return True
        for button in self._mouse_buttons:
            if input.is_mouse_pressed(button):
                return True
        return False

    def is_released(self, input: "Input") -> bool:
        for key in self._keys:
            if input.is_key_released(key):
                return True
        for button in self._mouse_buttons:
            if input.is_mouse_released(button):
                return True
        return False


def get_axis(negative: "Action", positive: "Action", input: "Input") -> float:
    return (1.0 if positive.is_down(input) else 0.0) - (1.0 if negative.is_down(input) else 0.0)

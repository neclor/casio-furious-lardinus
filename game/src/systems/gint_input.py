import gint
from gamekit.systems import key as Key
_KEY_MAP = {Key.LEFT: gint.KEY_LEFT, Key.RIGHT: gint.KEY_RIGHT, Key.UP: gint.KEY_UP, Key.ESCAPE: gint.KEY_EXIT, Key.AC: gint.KEY_ACON, Key.NUM_2: gint.KEY_2, Key.NUM_4: gint.KEY_4, Key.NUM_6: gint.KEY_6, Key.NUM_8: gint.KEY_8, Key.F1: gint.KEY_F1, Key.F2: gint.KEY_F2, Key.F3: gint.KEY_F3}
_NATIVE_TO_KEY = {native: key for key, native in _KEY_MAP.items()}
_down = set()
_pressed_this_frame = set()
_released_this_frame = set()

def poll():
    global _pressed_this_frame, _released_this_frame
    _pressed_this_frame = set()
    _released_this_frame = set()
    while True:
        event = gint.pollevent()
        if event.type == gint.KEYEV_NONE:
            break
        key = _NATIVE_TO_KEY.get(event.key)
        if key is None:
            continue
        if event.type == gint.KEYEV_DOWN:
            _down.add(key)
            _pressed_this_frame.add(key)
        elif event.type == gint.KEYEV_UP:
            _down.discard(key)
            _released_this_frame.add(key)

def is_key_down(key):
    return key in _down

def is_key_pressed(key):
    return key in _pressed_this_frame

def is_key_released(key):
    return key in _released_this_frame

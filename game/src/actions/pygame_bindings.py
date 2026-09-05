from gamekit.systems.input import Key, MouseButton

from actions.definitions import Actions


def bind() -> None:
    Actions.PAUSE.bind_key(Key.ESCAPE)
    Actions.FULL_SCREEN.bind_key(Key.F11)

    Actions.MOVE_FORWARD.bind_key(Key.W)
    Actions.MOVE_BACKWARD.bind_key(Key.S)
    Actions.MOVE_LEFT.bind_key(Key.A)
    Actions.MOVE_RIGHT.bind_key(Key.D)

    Actions.FIRE.bind_mouse_button(MouseButton.LEFT)
    Actions.WEAPON_GUN.bind_key(Key.NUM_1)
    Actions.WEAPON_SHOTGUN.bind_key(Key.NUM_2)
    Actions.WEAPON_ASSAULT.bind_key(Key.NUM_3)

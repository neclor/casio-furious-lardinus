from gamekit.systems import key as Key

from actions import definitions as Actions


def bind() -> None:
    Actions.QUIT.bind_key(Key.ESCAPE)
    Actions.PAUSE.bind_key(Key.AC)

    Actions.MOVE_FORWARD.bind_key(Key.NUM_8)
    Actions.MOVE_BACKWARD.bind_key(Key.NUM_2)
    Actions.MOVE_LEFT.bind_key(Key.NUM_4)
    Actions.MOVE_RIGHT.bind_key(Key.NUM_6)
    Actions.TURN_LEFT.bind_key(Key.LEFT)
    Actions.TURN_RIGHT.bind_key(Key.RIGHT)

    Actions.FIRE.bind_key(Key.UP)
    Actions.WEAPON_GUN.bind_key(Key.F1)
    Actions.WEAPON_SHOTGUN.bind_key(Key.F2)
    Actions.WEAPON_ASSAULT.bind_key(Key.F3)

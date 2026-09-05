from gamekit.systems.actions import Action


class Actions:
    QUIT: Action = Action()
    PAUSE: Action = Action()
    FULL_SCREEN: Action = Action()

    MOVE_FORWARD: Action = Action()
    MOVE_BACKWARD: Action = Action()
    MOVE_LEFT: Action = Action()
    MOVE_RIGHT: Action = Action()
    TURN_LEFT: Action = Action()
    TURN_RIGHT: Action = Action()

    FIRE: Action = Action()
    WEAPON_GUN: Action = Action()
    WEAPON_SHOTGUN: Action = Action()
    WEAPON_ASSAULT: Action = Action()

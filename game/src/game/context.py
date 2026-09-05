from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.game_root import GameRoot
    from game.world import World
    from game.levels.level import Level
    from game.weapons.weapon_manager import WeaponManager
    from game.objects.dynamic_objects.entities.player import Player


class GameContext:
    __slots__ = ("game", "world", "level", "weapon_manager", "player")

    game: "GameRoot"
    world: "World"
    level: "Level"
    weapon_manager: "WeaponManager"
    player: "Player"

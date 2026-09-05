TYPE_CHECKING = False

if TYPE_CHECKING:
    from flgame.game_root import GameRoot
    from flgame.world import World
    from flgame.levels.level import Level
    from flgame.weapons.weapon_manager import WeaponManager
    from flgame.objects.dynamic_objects.entities.player import Player


class GameContext:
    __slots__ = ("game", "world", "level", "weapon_manager", "player")

    game: "GameRoot"
    world: "World"
    level: "Level"
    weapon_manager: "WeaponManager"
    player: "Player"

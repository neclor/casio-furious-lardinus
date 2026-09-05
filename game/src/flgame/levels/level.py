from gamekit.math.vectors.vector2 import Vector2
from gamekit.systems.render.color import Color

import flgame.levels.layouts as Layouts
from flgame.context import GameContext
from flgame.levels.tiles import Tile, TileSet, build_tile_set

from flgame.objects.active_objects.ammo import Ammo
from flgame.objects.active_objects.medikit import Medikit
from flgame.objects.active_objects.exit import Exit
from flgame.objects.dynamic_objects.entities.enemies.knight import Knight
from flgame.objects.dynamic_objects.entities.enemies.skull import Skull
from flgame.objects.dynamic_objects.entities.enemies.summoner import Summoner
from flgame.objects.dynamic_objects.entities.enemies.wizzard import Wizzard

TYPE_CHECKING = False

if TYPE_CHECKING:
    from flgame.objects.game_object import GameObject


class Level:
    _LAYOUTS: list[str] = Layouts.CAMPAIGN
    _OBJECT_CLASSES: "dict[str, type[GameObject]]" = {
        "A": Ammo,
        "M": Medikit,
        "K": Knight,
        "C": Skull,
        "U": Summoner,
        "W": Wizzard,
        "E": Exit,
    }

    __slots__ = (
        "context",
        "current_index",
        "floor_color",
        "tile_size",
        "tile_map_size",
        "tile_map",
        "min_point_z",
        "max_point_z",
        "_tile_set",
    )

    context: GameContext
    current_index: int
    floor_color: Color
    tile_size: Vector2
    tile_map_size: Vector2
    tile_map: list[list[Tile | None]]
    min_point_z: float
    max_point_z: float
    _tile_set: TileSet


    def __init__(self, context: GameContext) -> None:
        self.context = context
        self.current_index = 0
        self._tile_set = build_tile_set()

        self.floor_color = Color.BLACK
        self.tile_size = self._tile_set.tile_size
        self.tile_map_size = Vector2()
        self.tile_map = []
        self.min_point_z = 0.0
        self.max_point_z = 0.0


    def load(self) -> None:
        spawn_point, level_objects = self._parse(self._LAYOUTS[self.current_index])

        self.context.player.position = spawn_point
        self.context.world.reset([self.context.player] + level_objects)


    def next(self) -> None:
        self.current_index = min(self.current_index + 1, len(self._LAYOUTS) - 1)
        self.load()


    def _parse(self, layout: str) -> "tuple[Vector2, list[GameObject]]":
        text = layout.replace(" ", "").replace("\t", "")
        text = text.replace("\n", "").replace("\r", "").rstrip("/")
        rows = text.split("/")

        self.floor_color = Color.from_hex(rows[1])
        self.tile_size = self._tile_set.tile_size
        self.tile_map_size = Vector2(len(rows[2]), len(rows) - 2)

        spawn_point = Vector2()
        self.min_point_z = 0.0
        self.max_point_z = 0.0
        self.tile_map = []
        level_objects: "list[GameObject]" = []

        for y, row in enumerate(rows[2:]):
            tile_row: list[Tile | None] = []
            for x, char in enumerate(row):
                center = Vector2(
                    x * self.tile_size.x + self.tile_size.x // 2,
                    y * self.tile_size.y + self.tile_size.y // 2,
                )
                if char == "S":
                    spawn_point = center

                tile = self._tile_set.get(char)
                tile_row.append(tile)
                if tile is not None:
                    bottom = tile.position_z
                    top = bottom - tile.height
                    self.min_point_z = min(top, bottom, self.min_point_z)
                    self.max_point_z = max(top, bottom, self.max_point_z)

                object_class = self._OBJECT_CLASSES.get(char)
                if object_class is not None:
                    level_objects.append(object_class(self.context, center))
            self.tile_map.append(tile_row)

        return spawn_point, level_objects

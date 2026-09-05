from gamekit.math.vectors import Vector2
from gamekit.systems.render.texture import Texture

from systems.services import services
import settings as Settings


class Tile:
    __slots__ = ("collision_layer", "collidable", "static", "transparent",
                 "texture", "position_z", "height")

    collision_mask: int = 0

    collision_layer: int
    collidable: bool
    static: bool
    transparent: bool
    texture: Texture
    position_z: float
    height: int


    def __init__(
        self,
        texture: Texture,
        *,
        collision_layer: int = Settings.WALL,
        collidable: bool = True,
        transparent: bool = False,
        position_z: float = 0.0,
        height: int = 128,
    ) -> None:
        self.texture = texture
        self.collision_layer = collision_layer
        self.collidable = collidable
        self.static = True
        self.transparent = transparent
        self.position_z = position_z
        self.height = height


class TileSet:
    __slots__ = ("tile_size", "_tiles")

    tile_size: Vector2
    _tiles: dict[str, Tile]


    def __init__(self, tile_size: Vector2, tiles: dict[str, Tile]) -> None:
        self.tile_size = tile_size
        self._tiles = tiles


    def get(self, char: str) -> Tile | None:
        return self._tiles.get(char)


def _load(name: str) -> Texture:
    return services.renderer.load_texture("src/assets/sprites/tiles/" + name)


def build_tile_set() -> TileSet:
    return TileSet(
        Vector2(64, 64),
        {
            "<": Tile(_load("wall_move.png")),
            "=": Tile(_load("wall_weapons.png")),
            "+": Tile(_load("wall_shoot.png")),
            ">": Tile(_load("wall_secret_tutorial.png")),
            "1": Tile(_load("wall_64_128.png")),
            "#": Tile(_load("wall_transparent.png"),
                      collision_layer=Settings.OBSTACLE, transparent=True),
            "?": Tile(_load("secret_wall_64_128.png"), collidable=False),
            "$": Tile(_load("secret_message.png")),
            "!": Tile(_load("end_tile.png")),
        },
    )

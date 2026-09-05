from gamekit.math.vectors.vector2 import Vector2

import systems.services as services
import settings as Settings

TYPE_CHECKING = False

if TYPE_CHECKING:
    from systems.gint_renderer import GintTexture


class Tile:
    __slots__ = ("collision_layer", "collidable", "static", "transparent",
                 "texture", "position_z", "height")

    collision_mask: int = 0

    collision_layer: int
    collidable: bool
    static: bool
    transparent: bool
    texture: "GintTexture"
    position_z: float
    height: int


    def __init__(
        self,
        texture: "GintTexture",
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
    __slots__ = ("tile_size", "_tiles", "_specs")

    tile_size: Vector2
    _tiles: dict[str, Tile]
    _specs: dict[str, tuple[str, dict]]


    def __init__(self, tile_size: Vector2, specs: dict[str, tuple[str, dict]]) -> None:
        self.tile_size = tile_size
        self._tiles = {}
        self._specs = specs


    def get(self, char: str) -> Tile | None:
        tile = self._tiles.get(char)
        if tile is not None:
            return tile

        spec = self._specs.get(char)
        if spec is None:
            return None

        name, kwargs = spec
        tile = Tile(_load(name), **kwargs)
        self._tiles[char] = tile
        return tile


def _load(name: str) -> "GintTexture":
    return services.renderer.load_texture("src/assets/sprites/tiles/" + name)


def build_tile_set() -> TileSet:
    # Textures are loaded lazily on first use (see TileSet.get) instead of all at
    # once here, since no single level layout uses every tile type.
    return TileSet(
        Vector2(64, 64),
        {
            "<": ("wall_move.png", {}),
            "=": ("wall_weapons.png", {}),
            "+": ("wall_shoot.png", {}),
            ">": ("wall_secret_tutorial.png", {}),
            "1": ("wall_64_128.png", {}),
            "#": ("wall_transparent.png",
                  {"collision_layer": Settings.OBSTACLE, "transparent": True}),
            "?": ("secret_wall_64_128.png", {"collidable": False}),
            "$": ("secret_message.png", {}),
            "!": ("end_tile.png", {}),
        },
    )

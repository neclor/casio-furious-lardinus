from gamekit.math.vectors.vector2 import Vector2

from game.context import GameContext
from game.levels.tiles import Tile

TYPE_CHECKING = False

if TYPE_CHECKING:
    from systems.gint_renderer import GintTexture


class GameObject:
    __slots__ = (
        "context",
        "freed",
        "collision_layer",
        "collision_mask",
        "collidable",
        "static",
        "position",
        "radius",
        "position_z",
        "height",
        "sprite",
    )

    context: GameContext
    freed: bool
    collision_layer: int
    collision_mask: int
    collidable: bool
    static: bool
    position: Vector2
    radius: int
    position_z: float
    height: int
    sprite: "GintTexture | None"


    def __init__(self, context: GameContext, position: Vector2) -> None:
        self.context = context
        self.freed = False

        self.collision_layer = 0
        self.collision_mask = 0
        self.collidable = False
        self.static = True

        self.position = Vector2(position)
        self.radius = 16

        self.position_z = 0.0
        self.height = 32

        self.sprite = None


    def update(self, delta: float) -> None:
        pass


    def on_collision(self, other: "GameObject | Tile") -> None:
        pass

from gamekit.math.vectors.vector2 import Vector2

from game.context import GameContext
from game.objects.game_object import GameObject


class DynamicObject(GameObject):
    __slots__ = ("velocity",)

    velocity: Vector2


    def __init__(
        self,
        context: GameContext,
        position: Vector2,
        velocity: Vector2 | None = None,
    ) -> None:
        super().__init__(context, position)
        self.static = False
        self.velocity = (
            Vector2(velocity) if velocity is not None else Vector2()
        )


    def _move_and_slide(self, delta: float) -> None:
        self.position += self.velocity * delta

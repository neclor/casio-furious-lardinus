from flgame.context import GameContext
from flgame.systems.object_manager import ObjectManager
from flgame.systems.physics_manager import PhysicsManager

TYPE_CHECKING = False

if TYPE_CHECKING:
    from flgame.objects.game_object import GameObject


class World:
    __slots__ = ("context", "objects_manager", "physics")

    context: GameContext
    objects_manager: ObjectManager
    physics: PhysicsManager


    def __init__(self, context: GameContext) -> None:
        self.context = context
        self.objects_manager = ObjectManager()
        self.physics = PhysicsManager(context)


    @property
    def objects(self) -> "list[GameObject]":
        return self.objects_manager.objects


    def reset(self, objects: "list[GameObject]") -> None:
        self.objects_manager.reset(objects)


    def add(self, game_object: "GameObject") -> None:
        self.objects_manager.add(game_object)


    def remove(self, game_object: "GameObject") -> None:
        self.objects_manager.remove(game_object)


    def update(self, delta: float) -> None:
        self.objects_manager.update(delta)
        self.physics.resolve(self.objects_manager.objects)
        self.objects_manager.flush()

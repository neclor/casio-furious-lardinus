import gc

from flgame.context import GameContext

TYPE_CHECKING = False

if TYPE_CHECKING:
    from flgame.objects.game_object import GameObject
    from flgame.systems.object_manager import ObjectManager
    from flgame.systems.physics_manager import PhysicsManager


class World:
    __slots__ = ("context", "objects_manager", "physics")

    context: GameContext
    objects_manager: "ObjectManager"
    physics: "PhysicsManager"


    def __init__(self, context: GameContext) -> None:
        self.context = context

        from flgame.systems.object_manager import ObjectManager
        self.objects_manager = ObjectManager()
        gc.collect()
        print("mem free (world.object_manager):", gc.mem_free())

        from flgame.systems.physics_manager import PhysicsManager
        self.physics = PhysicsManager(context)
        gc.collect()
        print("mem free (world.physics_manager):", gc.mem_free())


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

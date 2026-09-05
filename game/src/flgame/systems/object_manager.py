TYPE_CHECKING = False

if TYPE_CHECKING:
    from flgame.objects.game_object import GameObject


class ObjectManager:
    __slots__ = ("objects", "_add_queue", "_remove_queue")

    objects: "list[GameObject]"
    _add_queue: "list[GameObject]"
    _remove_queue: "list[GameObject]"


    def __init__(self) -> None:
        self.objects = []
        self._add_queue = []
        self._remove_queue = []


    def reset(self, objects: "list[GameObject]") -> None:
        self.objects = objects
        self._add_queue = []
        self._remove_queue = []


    def add(self, game_object: "GameObject") -> None:
        self._add_queue.append(game_object)


    def remove(self, game_object: "GameObject") -> None:
        game_object.freed = True
        self._remove_queue.append(game_object)


    def update(self, delta: float) -> None:
        game_object: "GameObject"
        for game_object in self.objects:
            if not game_object.freed:
                game_object.update(delta)


    def flush(self) -> None:
        self._flush_removals()
        self._flush_additions()


    def _flush_additions(self) -> None:
        self.objects += self._add_queue
        self._add_queue = []


    def _flush_removals(self) -> None:
        game_object: "GameObject"
        for game_object in self._remove_queue:
            if game_object in self.objects:
                self.objects.remove(game_object)
        self._remove_queue = []

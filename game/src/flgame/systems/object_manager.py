class ObjectManager:
    __slots__ = ('objects', '_add_queue', '_remove_queue')

    def __init__(self):
        self.objects = []
        self._add_queue = []
        self._remove_queue = []

    def reset(self, objects):
        self.objects = objects
        self._add_queue = []
        self._remove_queue = []

    def add(self, game_object):
        self._add_queue.append(game_object)

    def remove(self, game_object):
        game_object.freed = True
        self._remove_queue.append(game_object)

    def update(self, delta):
        for game_object in self.objects:
            if not game_object.freed:
                game_object.update(delta)

    def flush(self):
        self._flush_removals()
        self._flush_additions()

    def _flush_additions(self):
        self.objects += self._add_queue
        self._add_queue = []

    def _flush_removals(self):
        for game_object in self._remove_queue:
            if game_object in self.objects:
                self.objects.remove(game_object)
        self._remove_queue = []

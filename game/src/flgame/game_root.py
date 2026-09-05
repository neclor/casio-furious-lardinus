import gc
import systems.services as services
from actions import Actions

class GameRoot:
    __slots__ = ('_context', '_display', '_timer', '_paused')

    def __init__(self):
        self._timer = 0.0
        self._paused = False
        print('mem free (start):', gc.mem_free())
        from flgame.context import GameContext
        context = GameContext()
        gc.collect()
        print('mem free (context):', gc.mem_free())
        context.game = self
        from flgame.world import World
        context.world = World(context)
        gc.collect()
        print('mem free (world):', gc.mem_free())
        from flgame.levels.level import Level
        context.level = Level(context)
        gc.collect()
        print('mem free (level):', gc.mem_free())
        from flgame.weapons.weapon_manager import WeaponManager
        context.weapon_manager = WeaponManager(context)
        gc.collect()
        print('mem free (weapon_manager):', gc.mem_free())
        from gamekit.math.vectors.vector2 import Vector2
        from flgame.objects.dynamic_objects.entities.player import Player
        context.player = Player(context, Vector2())
        gc.collect()
        print('mem free (player):', gc.mem_free())
        self._context = context
        from flgame.rendering.display import Display
        self._display = Display(context)
        gc.collect()
        print('mem free (display):', gc.mem_free())
        context.level.load()
        gc.collect()
        print('mem free (level.load):', gc.mem_free())

    @property
    def timer(self):
        return self._timer

    def update(self, delta):
        if not self._paused:
            self._timer += delta
            self._context.weapon_manager.update(delta)
            self._context.world.update(delta)
        self._display.render()
        self._handle_events()

    def _handle_events(self):
        if Actions.PAUSE.is_pressed(services.input):
            self._toggle_pause()

    def _toggle_pause(self):
        self._paused = not self._paused

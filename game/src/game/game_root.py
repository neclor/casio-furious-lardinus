from gamekit.math.vectors import Vector2

from systems.services import services
from actions import Actions
from game.context import GameContext
from game.world import World
from game.levels.level import Level
from game.weapons.weapon_manager import WeaponManager
from game.rendering.display import Display
from game.objects.dynamic_objects.entities.player import Player


class GameRoot:
    __slots__ = ("_context", "_display", "_timer", "_paused")

    _context: GameContext
    _display: Display
    _timer: float
    _paused: bool

    def __init__(self) -> None:
        self._timer = 0.0
        self._paused = False
        self._set_mouse_visible(False)

        context: GameContext = GameContext()
        context.game = self
        context.world = World(context)
        context.level = Level(context)
        context.weapon_manager = WeaponManager(context)
        context.player = Player(context, Vector2())
        self._context = context

        self._display = Display(context)
        context.level.load()

    @property
    def timer(self) -> float:
        return self._timer

    def update(self, delta: float) -> None:
        if not self._paused:
            self._timer += delta
            self._context.weapon_manager.update(delta)
            self._context.world.update(delta)
        self._display.render()
        self._handle_events()

    def _handle_events(self) -> None:
        if Actions.PAUSE.is_pressed(services.input):
            self._toggle_pause()

    def _toggle_pause(self) -> None:
        self._paused = not self._paused
        self._set_mouse_visible(self._paused)

    @staticmethod
    def _set_mouse_visible(visible: bool) -> None:
        services.input.set_mouse_captured(not visible)

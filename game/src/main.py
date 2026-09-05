import sys

import settings as Settings
from actions import Actions
from actions.gint_bindings import bind as bind_actions

from systems.services import services
from systems.gint_renderer import create_renderer
from systems.gint_input import GintInput
from systems.gint_clock import GintClock

TYPE_CHECKING = False

if TYPE_CHECKING:
    from gamekit.systems.clock import Clock
    from game.game_root import GameRoot


class Game:
    __slots__ = ("_clock", "_root")

    _clock: "Clock"
    _root: "GameRoot"

    def __init__(self) -> None:
        services.renderer = create_renderer()
        services.input = GintInput()
        bind_actions()

        from game.game_root import GameRoot

        self._clock = GintClock()
        self._root = GameRoot()


    def run(self) -> None:
        while True:
            delta = self._clock.tick(Settings.tick_fps)
            Settings.current_fps = self._clock.get_fps()

            services.input.poll()
            self._handle_events()
            self._root.update(delta)


    def _handle_events(self) -> None:
        if services.input.should_quit() or Actions.QUIT.is_pressed(services.input):
            services.renderer.shutdown()
            sys.exit()


def main() -> None:
    Game().run()


if __name__ == "__main__": main()

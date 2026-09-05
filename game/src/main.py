import gc
import sys

import settings as Settings
from actions import Actions
from actions.gint_bindings import bind as bind_actions

import systems.services as services
from systems.gint_renderer import create_renderer
import systems.gint_input as gint_input
import systems.gint_clock as gint_clock

TYPE_CHECKING = False

if TYPE_CHECKING:
    from game.game_root import GameRoot


class Game:
    __slots__ = ("_root",)

    _root: "GameRoot"

    def __init__(self) -> None:
        services.renderer = create_renderer()
        services.input = gint_input
        bind_actions()

        from game.game_root import GameRoot

        self._root = GameRoot()


    def run(self) -> None:
        while True:
            delta = gint_clock.tick(Settings.tick_fps)
            Settings.current_fps = gint_clock.get_fps()

            services.input.poll()
            self._handle_events()
            self._root.update(delta)
            gc.collect()


    def _handle_events(self) -> None:
        if Actions.QUIT.is_pressed(services.input):
            services.renderer.shutdown()
            sys.exit()


def main() -> None:
    Game().run()


if __name__ == "__main__": main()

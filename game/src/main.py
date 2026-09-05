import gc
import sys

print("mem free (gc, sys):", gc.mem_free())

import settings as Settings
gc.collect()
print("mem free (settings):", gc.mem_free())

from actions import Actions
gc.collect()
print("mem free (actions):", gc.mem_free())

from actions.gint_bindings import bind as bind_actions
gc.collect()
print("mem free (gint_bindings):", gc.mem_free())

import systems.services as services
gc.collect()
print("mem free (services):", gc.mem_free())

from systems.gint_renderer import create_renderer
gc.collect()
print("mem free (gint_renderer):", gc.mem_free())

import systems.gint_input as gint_input
gc.collect()
print("mem free (gint_input):", gc.mem_free())

import systems.gint_clock as gint_clock
gc.collect()
print("mem free (gint_clock):", gc.mem_free())

from flgame.game_root import GameRoot
gc.collect()
print("mem free (game_root):", gc.mem_free())


class Game:
    __slots__ = ("_root",)

    _root: GameRoot

    def __init__(self) -> None:
        services.renderer = create_renderer()
        services.input = gint_input
        bind_actions()

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


main()

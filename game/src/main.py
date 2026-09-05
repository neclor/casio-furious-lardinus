import gc
import sys

print("1: gc, sys imported")

import settings as Settings

print("2: settings imported")

from actions import Actions

print("3: actions imported")

from actions.gint_bindings import bind as bind_actions

print("4: gint_bindings imported")

import systems.services as services

print("5: services imported")

from systems.gint_renderer import create_renderer

print("6: gint_renderer imported")

import systems.gint_input as gint_input

print("7: gint_input imported")

import systems.gint_clock as gint_clock

print("8: gint_clock imported")

TYPE_CHECKING = False

if TYPE_CHECKING:
    from game.game_root import GameRoot


class Game:
    __slots__ = ("_root",)

    _root: "GameRoot"

    def __init__(self) -> None:
        print("9: Game.__init__ start")

        services.renderer = create_renderer()
        print("10: renderer created")

        services.input = gint_input
        print("11: input set")

        bind_actions()
        print("12: actions bound")

        from game.game_root import GameRoot
        print("13: game_root imported")

        self._root = GameRoot()
        print("14: GameRoot() constructed")


    def run(self) -> None:
        print("15: entering main loop")
        frame = 0
        while True:
            delta = gint_clock.tick(Settings.tick_fps)
            Settings.current_fps = gint_clock.get_fps()

            services.input.poll()
            self._handle_events()
            self._root.update(delta)
            gc.collect()

            if frame < 5:
                print("16: frame", frame, "delta", delta)
            frame += 1


    def _handle_events(self) -> None:
        if Actions.QUIT.is_pressed(services.input):
            services.renderer.shutdown()
            sys.exit()


def main() -> None:
    print("0: main() start")
    Game().run()


if __name__ == "__main__": main()

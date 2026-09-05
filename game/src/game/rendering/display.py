from gamekit.systems.render.color import Color

import systems.services as services
from game.context import GameContext
from game.rendering.renderer_3d import Renderer3D
from game.rendering.hud import Hud


class Display:
    __slots__ = ("_renderer", "_hud")

    _renderer: Renderer3D
    _hud: Hud


    def __init__(self, context: GameContext) -> None:
        self._renderer = Renderer3D(context)
        self._hud = Hud(context)


    def render(self) -> None:
        services.renderer.clear(Color.BLACK)
        self._renderer.render()
        self._hud.render()
        services.renderer.update_screen()

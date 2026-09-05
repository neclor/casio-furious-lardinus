import gc

from gamekit.systems.render.color import Color

import systems.services as services
from flgame.context import GameContext

TYPE_CHECKING = False

if TYPE_CHECKING:
    from flgame.rendering.renderer_3d import Renderer3D
    from flgame.rendering.hud import Hud


class Display:
    __slots__ = ("_renderer", "_hud")

    _renderer: "Renderer3D"
    _hud: "Hud"


    def __init__(self, context: GameContext) -> None:
        from flgame.rendering.renderer_3d import Renderer3D
        self._renderer = Renderer3D(context)
        gc.collect()

        from flgame.rendering.hud import Hud
        self._hud = Hud(context)
        gc.collect()


    def render(self) -> None:
        services.renderer.clear(Color.BLACK)
        self._renderer.render()
        self._hud.render()
        services.renderer.update_screen()

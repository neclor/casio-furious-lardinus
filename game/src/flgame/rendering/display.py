import gc
from gamekit.systems.render.color import Color
import systems.services as services
from flgame.context import GameContext

class Display:
    __slots__ = ('_renderer', '_hud')

    def __init__(self, context):
        from flgame.rendering.renderer_3d import Renderer3D
        self._renderer = Renderer3D(context)
        gc.collect()
        from flgame.rendering.hud import Hud
        self._hud = Hud(context)
        gc.collect()

    def render(self):
        services.renderer.clear(Color.BLACK)
        self._renderer.render()
        self._hud.render()
        services.renderer.update_screen()

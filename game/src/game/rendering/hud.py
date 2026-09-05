from gamekit.math.vectors import Vector2
from gamekit.systems.render.color import Color
from gamekit.systems.render.font import Font

import settings as Settings
from systems.services import services
from game.context import GameContext


_FONT_SIZE: int = 24
_Z: int = 2


class Hud:
    __slots__ = ("context", "_font")

    context: GameContext
    _font: Font


    def __init__(self, context: GameContext) -> None:
        self.context = context
        self._font = services.renderer.load_font("src/assets/fonts/Pixel_Game.otf", _FONT_SIZE)


    def render(self) -> None:
        timer = self.context.game.timer
        weapon = self.context.weapon_manager.current
        half_w = Settings.half_resolution[0]
        res_w, res_h = Settings.resolution

        self._blit(f"{int(timer // 60)}:{int(timer % 60)}", half_w, 0, align_x="center")
        self._blit(str(self.context.player.health), half_w, res_h, align_x="center", align_y="bottom")
        self._blit(weapon.name, 0, res_h, align_y="bottom")
        self._blit(str(weapon.ammo), res_w, res_h, align_x="right", align_y="bottom")


    def _blit(self, text: str, x: float, y: float, align_x: str = "left", align_y: str = "top") -> None:
        size = self._font.measure(text)
        if align_x == "center":
            x -= size.x / 2
        elif align_x == "right":
            x -= size.x
        if align_y == "bottom":
            y -= size.y
        services.renderer.draw_text(self._font, text, Vector2(x, y), Color.WHITE, z=_Z)

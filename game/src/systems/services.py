TYPE_CHECKING = False

if TYPE_CHECKING:
    from gamekit.systems.input import Input
    from gamekit.systems.render.renderer import Renderer


class Services:
    __slots__ = ("renderer", "input")

    renderer: "Renderer"
    input: "Input"


services = Services()

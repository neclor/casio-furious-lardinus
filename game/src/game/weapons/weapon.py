TYPE_CHECKING = False

if TYPE_CHECKING:
    from systems.gint_renderer import GintTexture


class Weapon:
    __slots__ = ("name", "available", "sprite", "damage", "max_ammo", "ammo", "cooldown")

    name: str
    available: bool
    sprite: "GintTexture | None"
    damage: int
    max_ammo: float
    ammo: float
    cooldown: float


    def __init__(
        self,
        name: str,
        damage: int,
        max_ammo: float,
        cooldown: float,
        available: bool = True,
    ) -> None:
        self.name = name
        self.available = available
        self.sprite = None
        self.damage = damage
        self.max_ammo = max_ammo
        self.ammo = max_ammo
        self.cooldown = cooldown

class Weapon:
    __slots__ = ('name', 'available', 'sprite', 'damage', 'max_ammo', 'ammo', 'cooldown')

    def __init__(self, name, damage, max_ammo, cooldown, available=True):
        self.name = name
        self.available = available
        self.sprite = None
        self.damage = damage
        self.max_ammo = max_ammo
        self.ammo = max_ammo
        self.cooldown = cooldown

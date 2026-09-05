from gamekit.math.vectors.vector2 import Vector2
import systems.services as services
import settings as Settings

class Tile:
    __slots__ = ('collision_layer', 'collidable', 'static', 'transparent', 'texture', 'position_z', 'height')
    collision_mask = 0

    def __init__(self, texture, *, collision_layer=Settings.WALL, collidable=True, transparent=False, position_z=0.0, height=128):
        self.texture = texture
        self.collision_layer = collision_layer
        self.collidable = collidable
        self.static = True
        self.transparent = transparent
        self.position_z = position_z
        self.height = height

class TileSet:
    __slots__ = ('tile_size', '_tiles', '_specs')

    def __init__(self, tile_size, specs):
        self.tile_size = tile_size
        self._tiles = {}
        self._specs = specs

    def get(self, char):
        tile = self._tiles.get(char)
        if tile is not None:
            return tile
        spec = self._specs.get(char)
        if spec is None:
            return None
        name, kwargs = spec
        tile = Tile(_load(name), **kwargs)
        self._tiles[char] = tile
        return tile

def _load(name):
    return services.renderer.load_texture('src/assets/sprites/tiles/' + name)

def build_tile_set():
    return TileSet(Vector2(64, 64), {'<': ('wall_16.png', {}), '=': ('wall_16.png', {}), '+': ('wall_16.png', {}), '>': ('wall_16.png', {}), '1': ('wall_16.png', {}), '#': ('wall_transparent_16.png', {'collision_layer': Settings.OBSTACLE, 'transparent': True}), '?': ('secret_wall_16.png', {'collidable': False}), '$': ('wall_16.png', {}), '!': ('wall_16.png', {})})

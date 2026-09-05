
import math

from gamekit.math.vectors.vector2 import Vector2
from gamekit.math.rects import Rect2, Rect2i
from gamekit.systems.render.texture import Texture

import settings as Settings
from systems.services import services
from game.context import GameContext
from game.objects.game_object import GameObject


_MIN_RAY_COUNT: int = 64
_MAX_RAY_COUNT: int = Settings.resolution[0]

_Projection = tuple[Texture, Rect2i | None, Rect2, bool, float]


class Renderer3D:
    __slots__ = (
        "context",
        "_ray_count",
        "_ray_step_angle",
        "_ray_step_angle_tan",
        "_adjust_ray_counter",
        "_position",
        "_rotation",
        "_rotation_tan",
        "_camera_position_z",
    )

    context: GameContext
    _ray_count: int
    _ray_step_angle: float
    _ray_step_angle_tan: float
    _adjust_ray_counter: int
    _position: Vector2
    _rotation: float
    _rotation_tan: float
    _camera_position_z: float


    def __init__(self, context: GameContext) -> None:
        self.context = context

        self._ray_count = (_MAX_RAY_COUNT - _MIN_RAY_COUNT) // 2
        self._adjust_ray_counter = 0
        self._ray_step_angle = 0.0
        self._ray_step_angle_tan = 0.0
        self._update_ray_parameters()

        self._position = Vector2()
        self._rotation = 0.0
        self._rotation_tan = 0.0
        self._camera_position_z = 0.0


    def render(self) -> None:
        self._adjust_ray_count()
        self._update_camera()
        self._draw_floor()
        self._draw_game()


    def _update_ray_parameters(self) -> None:
        self._ray_step_angle = Settings.fov_h / self._ray_count
        self._ray_step_angle_tan = math.tan(self._ray_step_angle)


    def _adjust_ray_count(self) -> None:
        self._adjust_ray_counter += 1
        if self._adjust_ray_counter < 10:
            return
        self._adjust_ray_counter = 0

        if Settings.current_fps < Settings.fps and self._ray_count > _MIN_RAY_COUNT:
            self._ray_count -= 8
        elif (
            Settings.current_fps > Settings.max_fps_limit
            and self._ray_count < _MAX_RAY_COUNT
        ):
            self._ray_count += 8
        else:
            return
        self._update_ray_parameters()


    def _update_camera(self) -> None:
        player = self.context.player
        self._position = player.position
        self._rotation = player.rotation
        self._rotation_tan = math.tan(self._rotation)
        self._camera_position_z = player.position_z - player.height


    def _draw_floor(self) -> None:
        services.renderer.draw_rect(
            Rect2(
                0,
                Settings.half_resolution[1],
                Settings.resolution[0],
                Settings.half_resolution[1],
            ),
            self.context.level.floor_color,
            z=0,
        )


    def _draw_game(self) -> None:
        projections: list[_Projection] = (
            self._object_projections() + self._tile_map_projections()
        )
        projections.sort(key=lambda p: p[4], reverse=True)
        for texture, src, destination, flip_v, _distance in projections:
            services.renderer.draw_texture(texture, destination, src=src, flip_v=flip_v, z=1)


    def _object_projections(self) -> list[_Projection]:
        result: list[_Projection] = []
        for game_object in self.context.world.objects:
            projection = self._object_projection(game_object)
            if projection is not None:
                result.append(projection)
        return result


    def _object_projection(self, game_object: GameObject) -> _Projection | None:
        if game_object.sprite is None:
            return None

        radius = game_object.radius
        relative = Vector2(game_object.position - self._position).rotated(
            -self._rotation - Settings.HALF_PI
        )
        relative.y *= -1
        if relative.y <= 1:
            return None

        tan_left = (relative.x - radius) / relative.y
        tan_right = (relative.x + radius) / relative.y
        if (
            max(tan_left, tan_right) <= -Settings.tan_half_fov_h
            or min(tan_left, tan_right) >= Settings.tan_half_fov_h
        ):
            return None

        relative_bottom = game_object.position_z - self._camera_position_z
        relative_top = relative_bottom - game_object.height
        return self._calculate_projection(
            tan_left, tan_right, relative.y, relative_top, relative_bottom,
            game_object.sprite,
        )


    def _tile_map_projections(self) -> list[_Projection]:
        result: list[_Projection] = []
        ray_rotation = self._rotation - Settings.half_fov_h
        for _ in range(self._ray_count):
            result += self._cast_ray(ray_rotation)
            ray_rotation += self._ray_step_angle
        return result


    def _cast_ray(self, ray_rotation: float) -> list[_Projection]:
        level = self.context.level
        tile_size = level.tile_size
        map_size = level.tile_map_size
        position = self._position
        camera_z = self._camera_position_z

        tile_projections: list[_Projection] = []

        ray_relative_angle = ray_rotation - self._rotation
        ray_rotation = ray_rotation % (2 * math.pi)
        ray_sign = Vector2(
            (Settings.THREE_HALF_PI < ray_rotation <= (2 * math.pi)
             or 0 <= ray_rotation < Settings.HALF_PI)
            - (Settings.HALF_PI < ray_rotation < Settings.THREE_HALF_PI),
            (0 < ray_rotation < math.pi) - (math.pi < ray_rotation < (2 * math.pi)),
        )
        signed_tile_size = Vector2(
            ray_sign.x * tile_size.x, ray_sign.y * tile_size.y
        )

        ray_tan = math.tan(ray_rotation)
        abs_ray_tan = abs(ray_tan)
        ray_relative_angle_cos = math.cos(ray_relative_angle)
        ray_relative_angle_tan = (ray_tan - self._rotation_tan) / (
            1 + ray_tan * self._rotation_tan
        )
        right_ray_relative_angle_tan = (
            ray_relative_angle_tan + self._ray_step_angle_tan
        ) / (1 - ray_relative_angle_tan * self._ray_step_angle_tan)

        ray_position = position

        x_whole, x_fractional = divmod(ray_position.x, tile_size.x)
        y_whole, y_fractional = divmod(ray_position.y, tile_size.y)
        tile_index = Vector2(
            x_whole - (ray_sign.x < 0 and x_fractional == 0),
            y_whole - (ray_sign.y < 0 and y_fractional == 0),
        )
        next_line = Vector2(
            (tile_index.x + (0 <= ray_sign.x)) * tile_size.x,
            (tile_index.y + (0 <= ray_sign.y)) * tile_size.y,
        )

        tan_min_obscured_angle = Settings.tan_half_fov_v
        tan_max_obscured_angle = -1 * Settings.tan_half_fov_v
        while not self._line_out_of_bounds(ray_sign, tile_index, map_size):
            delta_next_line = next_line - ray_position
            delta_ratio = (
                delta_next_line.y / delta_next_line.x
                if delta_next_line.x != 0
                else float("inf")
            )
            tan_delta_difference = abs_ray_tan - abs(delta_ratio)
            if tan_delta_difference < 0:
                ray_position = Vector2(
                    next_line.x, position.y + (next_line.x - position.x) * ray_tan
                )
                next_line.x += signed_tile_size.x
                tile_index.x += ray_sign.x
            elif tan_delta_difference > 0:
                ray_position = Vector2(
                    position.x + (next_line.y - position.y) / ray_tan, next_line.y
                )
                next_line.y += signed_tile_size.y
                tile_index.y += ray_sign.y
            else:
                ray_position = Vector2(next_line.x, next_line.y)
                next_line += signed_tile_size
                tile_index += ray_sign

            distance = (ray_position - position).length()

            relative_min_obscured_point = distance * tan_min_obscured_angle
            relative_max_obscured_point = distance * tan_max_obscured_angle
            if (
                relative_min_obscured_point <= level.min_point_z - camera_z
                and level.max_point_z - camera_z <= relative_max_obscured_point
            ):
                break

            if not (0 <= tile_index.x < map_size.x and 0 <= tile_index.y < map_size.y): continue

            tile = level.tile_map[int(tile_index.y)][int(tile_index.x)]

            if tile is None: continue

            tile_height = tile.height
            relative_tile_bottom = tile.position_z - camera_z
            relative_tile_top = relative_tile_bottom - tile_height

            relative_min_tile_point = min(relative_tile_top, relative_tile_bottom)
            relative_max_tile_point = max(relative_tile_top, relative_tile_bottom)

            min_tile_point_visible = relative_min_tile_point < relative_min_obscured_point
            max_tile_point_visible = relative_max_tile_point > relative_max_obscured_point
            if not (min_tile_point_visible or max_tile_point_visible): continue
            if not tile.transparent:
                if min_tile_point_visible:
                    tan_min_obscured_angle = relative_min_tile_point / distance
                if max_tile_point_visible:
                    tan_max_obscured_angle = relative_max_tile_point / distance

            texture_offset_x = abs(
                (ray_position.x % tile_size.x) / tile_size.x - max(ray_sign.y, 0)
            ) % 1
            texture_offset_y = abs(
                (ray_position.y % tile_size.y) / tile_size.y + min(ray_sign.x, 0)
            ) % 1
            x_offset_larger_y_offset = texture_offset_x > texture_offset_y
            texture_offset = (
                texture_offset_x if x_offset_larger_y_offset else texture_offset_y
            )

            texture = tile.texture
            texture_x = min(int(texture_offset * texture.width), texture.width - 1)
            column_src = Rect2i(texture_x, 0, 1, texture.height)

            tile_projections.append(
                self._calculate_projection(
                    ray_relative_angle_tan,
                    right_ray_relative_angle_tan,
                    distance * ray_relative_angle_cos,
                    relative_tile_top,
                    relative_tile_bottom,
                    texture,
                    column_src,
                )
            )
        return tile_projections


    @staticmethod
    def _line_out_of_bounds(
        ray_sign: Vector2, tile_index: Vector2, map_size: Vector2
    ) -> bool:
        return (
            (ray_sign.x < 0 and tile_index.x < 0)
            or (ray_sign.y < 0 and tile_index.y < 0)
            or (0 < ray_sign.x and map_size.x <= tile_index.x)
            or (0 < ray_sign.y and map_size.y <= tile_index.y)
        )


    @staticmethod
    def _calculate_projection(
        left_tan: float,
        right_tan: float,
        distance: float,
        relative_top: float,
        relative_bottom: float,
        texture: Texture,
        src: Rect2i | None = None,
    ) -> _Projection:
        factor = Settings.resolution_x_div_double_tan_half_fov_h
        position_x = left_tan * factor + Settings.half_resolution[0]
        width = right_tan * factor + Settings.half_resolution[0] - position_x

        position_y = 0.0
        height = 0.0
        flip_v = False
        if distance >= 1:
            if relative_bottom < relative_top:
                relative_top, relative_bottom = relative_bottom, relative_top
                flip_v = True

            y_factor = factor / distance
            position_y = relative_top * y_factor + Settings.half_resolution[1]
            height = (
                relative_bottom * y_factor + Settings.half_resolution[1] - position_y
            )

        return (
            texture,
            src,
            Rect2(math.floor(position_x), math.floor(position_y), math.ceil(width), math.ceil(height)),
            flip_v,
            distance,
        )

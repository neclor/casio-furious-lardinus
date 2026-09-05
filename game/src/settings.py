import math
from gamekit.math.utils import clampf
NAME = 'Furious Lardinus'
resolution = (128, 64)
fps = 30
fov_h = 2 * math.pi / 3
MIN_FOV_H = math.pi / 3
MAX_FOV_H = 2 * math.pi / 3
fps_amplitude = 20
current_fps = fps
WALL = 1
OBSTACLE = 2
ACTIVE = 4
ENEMY = 8
PLAYER = 16
PROJECTILE = 32
HALF_PI = math.pi / 2
THREE_HALF_PI = 3 * HALF_PI

def calculate_resolution_parameters():
    global half_resolution, aspect_ratio
    half_resolution = (resolution[0] // 2, resolution[1] // 2)
    aspect_ratio = resolution[0] / resolution[1]
    calculate_fov_parameters()

def calculate_fov_parameters():
    global fov_h, fov_v, half_fov_h, half_fov_v, tan_half_fov_h, tan_half_fov_v, double_tan_half_fov_h, double_tan_half_fov_v, resolution_x_div_double_tan_half_fov_h, resolution_y_div_double_tan_half_fov_v
    fov_h = clampf(fov_h, MIN_FOV_H, MAX_FOV_H)
    fov_v = 2 * math.atan(math.tan(fov_h / 2) / aspect_ratio)
    half_fov_h = fov_h / 2
    half_fov_v = fov_v / 2
    tan_half_fov_h = math.tan(half_fov_h)
    tan_half_fov_v = math.tan(half_fov_v)
    double_tan_half_fov_h = tan_half_fov_h * 2
    double_tan_half_fov_v = tan_half_fov_v * 2
    resolution_x_div_double_tan_half_fov_h = resolution[0] / double_tan_half_fov_h
    resolution_y_div_double_tan_half_fov_v = resolution[1] / double_tan_half_fov_v

def calculate_fps_parameters():
    global max_fps_limit, tick_fps
    max_fps_limit = fps + fps_amplitude
    tick_fps = fps + 2 * fps_amplitude
calculate_resolution_parameters()
calculate_fps_parameters()

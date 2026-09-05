import math
CMP_EPSILON = 1e-05
INT_MIN = -2147483648
INT_MAX = 2147483647

def lerp(a, b, t):
    return a + (b - a) * t

def clampf(v, lo, hi):
    return lo if v < lo else hi if v > hi else v

def round_half_away(v):
    return float(math.floor(v + 0.5)) if v >= 0.0 else float(math.ceil(v - 0.5))

def idiv(a, b):
    q = abs(a) // abs(b)
    return -q if (a < 0) != (b < 0) else q

def imod(a, b):
    return a - idiv(a, b) * b

def is_equal_approx(a, b):
    if a == b:
        return True
    tol = CMP_EPSILON * abs(a)
    if tol < CMP_EPSILON:
        tol = CMP_EPSILON
    return abs(a - b) < tol

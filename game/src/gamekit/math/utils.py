import math

CMP_EPSILON: float = 1e-05

INT_MIN: int = -2147483648
INT_MAX: int = 2147483647


def lerp(a: float, b: float, t: float) -> float: return a + (b - a) * t

def clampf(v: float, lo: float, hi: float) -> float: return lo if v < lo else (hi if v > hi else v)

def round_half_away(v: float) -> float: return float(math.floor(v + 0.5)) if v >= 0.0 else float(math.ceil(v - 0.5))

def idiv(a: int, b: int) -> int:
    q = abs(a) // abs(b)
    return -q if (a < 0) != (b < 0) else q


def imod(a: int, b: int) -> int: return a - idiv(a, b) * b


def is_equal_approx(a: float, b: float) -> bool:
    if a == b: return True

    tol = CMP_EPSILON * abs(a)
    if tol < CMP_EPSILON:
        tol = CMP_EPSILON

    return abs(a - b) < tol

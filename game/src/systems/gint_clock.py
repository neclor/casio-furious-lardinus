import time

_last: int = time.ticks_ms()
_fps: float = 0.0


def tick(fps: int) -> float:
    global _last, _fps

    if fps > 0:
        target_ms = 1000 // fps
        elapsed_ms = time.ticks_diff(time.ticks_ms(), _last)
        remaining_ms = target_ms - elapsed_ms
        if remaining_ms > 0:
            time.sleep_ms(remaining_ms)

    now = time.ticks_ms()
    delta_ms = time.ticks_diff(now, _last)
    _last = now
    delta = delta_ms / 1000.0
    _fps = 1000.0 / delta_ms if delta_ms > 0 else 0.0
    return delta


def get_fps() -> float:
    return _fps

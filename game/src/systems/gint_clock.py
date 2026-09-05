import time

from gamekit.systems.clock import Clock


class GintClock(Clock):
    __slots__ = ("_last", "_fps")

    _last: int
    _fps: float

    def __init__(self) -> None:
        self._last = time.ticks_ms()
        self._fps = 0.0

    def tick(self, fps: int) -> float:
        if fps > 0:
            target_ms = 1000 // fps
            elapsed_ms = time.ticks_diff(time.ticks_ms(), self._last)
            remaining_ms = target_ms - elapsed_ms
            if remaining_ms > 0:
                time.sleep_ms(remaining_ms)

        now = time.ticks_ms()
        delta_ms = time.ticks_diff(now, self._last)
        self._last = now
        delta = delta_ms / 1000.0
        self._fps = 1000.0 / delta_ms if delta_ms > 0 else 0.0
        return delta

    def get_fps(self) -> float:
        return self._fps

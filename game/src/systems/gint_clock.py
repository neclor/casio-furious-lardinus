import time

from gamekit.systems.clock import Clock


class GintClock(Clock):
    __slots__ = ("_last", "_fps")

    _last: float
    _fps: float

    def __init__(self) -> None:
        self._last = time.monotonic()
        self._fps = 0.0

    def tick(self, fps: int) -> float:
        if fps > 0:
            target = 1.0 / fps
            remaining = target - (time.monotonic() - self._last)
            if remaining > 0:
                time.sleep(remaining)

        now = time.monotonic()
        delta = now - self._last
        self._last = now
        self._fps = 1.0 / delta if delta > 0 else 0.0
        return delta

    def get_fps(self) -> float:
        return self._fps

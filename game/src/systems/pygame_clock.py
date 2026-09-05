import pygame

from gamekit.systems.clock import Clock


class PygameClock(Clock):
    __slots__ = ("_clock",)

    _clock: pygame.time.Clock

    def __init__(self) -> None:
        self._clock = pygame.time.Clock()

    def tick(self, fps: int) -> float:
        self._clock.tick(fps)
        return self._clock.get_time() / 1000

    def get_fps(self) -> float:
        return self._clock.get_fps()

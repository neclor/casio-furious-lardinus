class Clock:
    __slots__ = ()

    def tick(self, fps: int) -> float: raise NotImplementedError

    def get_fps(self) -> float: raise NotImplementedError

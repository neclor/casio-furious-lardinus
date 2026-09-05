class Action:
    __slots__ = ('_key',)

    def __init__(self):
        self._key = -1

    def bind_key(self, key):
        self._key = key
        return self

    def is_down(self, input):
        return self._key != -1 and input.is_key_down(self._key)

    def is_pressed(self, input):
        return self._key != -1 and input.is_key_pressed(self._key)

    def is_released(self, input):
        return self._key != -1 and input.is_key_released(self._key)

def get_axis(negative, positive, input):
    return (1.0 if positive.is_down(input) else 0.0) - (1.0 if negative.is_down(input) else 0.0)

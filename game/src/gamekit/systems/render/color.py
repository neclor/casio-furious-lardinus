class Color:
    __slots__ = ("r", "g", "b", "a")

    r: int
    g: int
    b: int
    a: int

    WHITE: "Color"
    BLACK: "Color"
    RED: "Color"
    GREEN: "Color"
    BLUE: "Color"
    TRANSPARENT: "Color"

    def __init__(self, r: int = 0, g: int = 0, b: int = 0, a: int = 255) -> None:
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)
        self.a = int(a)

    def with_a(self, a: int) -> "Color": return Color(self.r, self.g, self.b, a)

    @staticmethod
    def from_hex(value: str) -> "Color":
        text = value.lstrip("#")
        r = int(text[0:2], 16)
        g = int(text[2:4], 16)
        b = int(text[4:6], 16)
        a = int(text[6:8], 16) if len(text) >= 8 else 255
        return Color(r, g, b, a)

    def to_tuple(self) -> "tuple[int, int, int, int]": return (self.r, self.g, self.b, self.a)

    def __eq__(self, o: object) -> bool: return isinstance(o, Color) and self.r == o.r and self.g == o.g and self.b == o.b and self.a == o.a

    def __ne__(self, o: object) -> bool: return not (isinstance(o, Color) and self.r == o.r and self.g == o.g and self.b == o.b and self.a == o.a)

    def __hash__(self) -> int: return hash((self.r, self.g, self.b, self.a))

    def __repr__(self) -> str: return "Color({}, {}, {}, {})".format(self.r, self.g, self.b, self.a)


Color.WHITE = Color(255, 255, 255, 255)
Color.BLACK = Color(0, 0, 0, 255)
Color.RED = Color(255, 0, 0, 255)
Color.GREEN = Color(0, 255, 0, 255)
Color.BLUE = Color(0, 0, 255, 255)
Color.TRANSPARENT = Color(0, 0, 0, 0)

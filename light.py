from color import Color

class Light:
    """A point light source of given color, white by default"""
    def __init__(self,position,color = Color.from_hex("#FFFFFF")):
        self.position = position
        self.color = color
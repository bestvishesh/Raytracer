class Ray:
    """Line with an origin and direction"""
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normalize()
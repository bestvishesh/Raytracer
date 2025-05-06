import math # Added import
from color import Color


class Material:
    """Material has color and characteristics which tell how it reacts to light."""

    def __init__(self, color=Color.from_hex("#FFFFFF"), ambient=0.05, diffuse=1, specular=1, reflection = 0.5):
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection

    def color_at(self, position):
        return self.color

class CheckeredMaterial:
    """Material with checkered pattern."""

    def __init__(self, color1=Color.from_hex("#FFFFFF"), color2=Color.from_hex("#000000"), ambient=0.05, diffuse=1, specular=1, reflection = 0.5):
        self.color1 = color1
        self.color2 = color2
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection

    def color_at(self, position):
        if int((position.x+5)*3) %2 == int((position.z)*3) %2:
            return self.color1
        else:
            return self.color2


class LollipopMaterial:
    """Material with striped pattern."""

    def __init__(self, color1=Color.from_hex("#FFFFFF"), color2=Color.from_hex("#000000"), ambient=0.05, diffuse=1, specular=1, reflection = 0.5):
        self.color1 = color1
        self.color2 = color2
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection

    def color_at(self, position):
        if int(position.x * 2) % 2 == 0:
            return self.color1
        else:
            return self.color2


class PSMaterial:
    """Material with a pattern resembling PlayStation controller symbols."""

    def __init__(self, color_x=Color.from_hex("#0000FF"), color_o=Color.from_hex("#FF0000"),
                 color_box=Color.from_hex("#FFC0CB"), color_triangle=Color.from_hex("#00FF00"),
                 background_color=Color.from_hex("#FFFFFF"), scale=1.0,
                 ambient=0.05, diffuse=1.0, specular=1.0, reflection=0.5):

        if scale <= 0:
            raise ValueError("Scale must be positive.")

        self.color_x = color_x
        self.color_o = color_o
        self.color_box = color_box
        self.color_triangle = color_triangle
        self.background_color = background_color # Stored but not used in color_at
        self.scale = scale
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection

    def color_at(self, position):
        """Determines the color based on the xz-coordinates and scale."""
        cell_x = math.floor(position.x / self.scale)
        cell_z = math.floor(position.z / self.scale)

        if cell_x % 2 == 0:
            if cell_z % 2 == 0:
                return self.color_x
            else: # cell_z is odd
                return self.color_box
        else: # cell_x is odd
            if cell_z % 2 == 0:
                return self.color_o
            else: # cell_z is odd
                return self.color_triangle

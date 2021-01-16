from vector import Vector
from color import Color
from point import Point
from sphere import Sphere
from ray import Ray
from light import Light
from material import Material, CheckeredMaterial

WIDTH = 960
HEIGHT = 540
RENDERED_IMG = "blueBalls.ppm"
CAMERA = Vector(0, -0.35, -1)
OBJECTS = [
    # Ground Plane
    Sphere(Point(0, 10000.5, 1), 10000, CheckeredMaterial(color1=Color.from_hex("#440800"),
                                                           color2=Color.from_hex("#E5B87C"), 
                                                           ambient=0.3, reflection=0.2)),

    # Blue Ball 1
    Sphere(Point(0.6, -0.1, 1), 0.5, Material(Color.from_hex("#FFFF00"))),
    # Ball 2
    Sphere(Point(-0.6, -0.1, 2.5), 0.5, Material(Color.from_hex("#0000FF"))),
    # Mirror
    Sphere(Point(0, -0.1, 1.5), 0.5, Material(Color.from_hex("#FFFFFF"), reflection=0.9))
]
LIGHTS = [
    Light(Point(1.5, 0.5, 1), Color.from_hex("#FFFFFF")),
    Light(Point(-0.5, -10.5, 0), Color.from_hex("#E6E6E6"))
]

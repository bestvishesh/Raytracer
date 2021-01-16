from vector import Vector
from color import Color
from point import Point
from sphere import Sphere
from ray import Ray
from light import Light
from material import Material

WIDTH = 320
HEIGHT = 200
RENDERED_IMG = "first_one.ppm"
CAMERA = Vector(0, 0, -1)
OBJECTS = [Sphere(Point(0, -0.35, 0), 0.15, Material(Color.from_hex("#FF0000"))),
           Sphere(Point(0, 0, 0), 0.15, Material(Color.from_hex("#00FF00"))),
           Sphere(Point(0, 0.35, 0), 0.15, Material(Color.from_hex("#0000FF")))]
LIGHTS = [Light(Point(1.5, -0.5, -10), Color.from_hex("#FFFFFF"))]
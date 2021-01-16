from math import sqrt

class Sphere:
    """3D shape. Has centre, radius and material"""

    def __init__(self, centre, radius, material):
        self.centre = centre
        self.radius = radius
        self.material = material

    def intersects(self, ray):
        """Checks if the ray intersects with sphere.
        Returns distance to intersection or None if there is no intersection"""
        sphere_to_ray = ray.origin - self.centre
        b = 2 * ray.direction.dot_product(sphere_to_ray)
        c = sphere_to_ray.dot_product(sphere_to_ray) - self.radius*self.radius
        discriminant = b*b - 4*c
        if discriminant>=0:
            dist = (-b - sqrt(discriminant))/2
            if dist>0:
                return dist
        return None
    def normal(self, surface_point):
        """Returns surface normal to the point on Sphere's surface"""
        return  (surface_point-self.centre).normalize()
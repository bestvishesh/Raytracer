from point import Point
from vector import Vector
from material import Material # Assuming Material might be needed for type hinting or future use

class Square:
    """Represents an axis-aligned square on the xz-plane."""

    def __init__(self, center: Point, size: float, material: Material):
        """
        Initializes the Square.

        Args:
            center: The center point of the square (Point). The square lies on the y = center.y plane.
            size: The side length of the square (float).
            material: The material of the square.
        """
        self.center = center
        self.size = size
        self.material = material
        self.half_size = size / 2.0

    def intersects(self, ray):
        """
        Checks if the ray intersects with the square.

        Args:
            ray: The ray to check intersection with.

        Returns:
            The distance t to the intersection point if the ray intersects the square,
            otherwise None.
        """
        # Check if ray is parallel to the xz-plane
        if abs(ray.direction.y) < 1e-6: # Use a small epsilon for floating point comparison
            return None

        # Calculate intersection parameter t with the plane y = center.y
        t = (self.center.y - ray.origin.y) / ray.direction.y

        # Check if intersection is behind the ray origin
        if t < 1e-6: # Use epsilon here too, intersection must be in front
            return None

        # Calculate the intersection point
        p = ray.origin + ray.direction * t

        # Check if the intersection point is within the square's boundaries
        # Calculate the difference vector from the center to the intersection point
        delta = p - self.center

        # Check x and z boundaries
        if abs(delta.x) > self.half_size or abs(delta.z) > self.half_size:
            return None

        # Intersection is valid and within boundaries
        return t

    def normal(self, surface_point):
        """
        Returns the surface normal vector at a given point on the square's surface.
        For an axis-aligned square on the xz-plane, the normal is always (0, 1, 0).

        Args:
            surface_point: The point on the square's surface (unused for this simple case).

        Returns:
            The normal vector (Vector(0, 1, 0)).
        """
        # The normal is always pointing up for a square on the xz-plane
        return Vector(0, 1, 0)

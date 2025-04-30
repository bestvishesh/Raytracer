import math
from point import Point
from vector import Vector
from material import Material

class Cube:
    """Represents an axis-aligned cube."""

    def __init__(self, center: Point, size: float, material: Material):
        """
        Initializes the Cube.

        Args:
            center: The center point of the cube (Point).
            size: The side length of the cube (float).
            material: The material of the cube.
        """
        self.center = center
        self.size = size
        self.material = material
        half_size = size / 2.0
        # Calculate min and max extents as Vectors relative to origin for easier slab calculation
        self.min_extent = center - Vector(half_size, half_size, half_size)
        self.max_extent = center + Vector(half_size, half_size, half_size)
        # Store extents also as Points if needed, though Vectors might be sufficient
        # self.min_extent_p = Point(center.x - half_size, center.y - half_size, center.z - half_size)
        # self.max_extent_p = Point(center.x + half_size, center.y + half_size, center.z + half_size)

    def intersects(self, ray):
        """
        Checks if the ray intersects with the cube using the slab method.

        Args:
            ray: The ray to check intersection with.

        Returns:
            The distance t to the first intersection point if the ray intersects the cube,
            otherwise None.
        """
        tmin = float('-inf')
        tmax = float('inf')
        epsilon = 1e-6

        ray_origin_vec = Vector(ray.origin.x, ray.origin.y, ray.origin.z) # Work with vectors

        for i in range(3): # Iterate through x, y, z axes (0, 1, 2)
            axis_origin = ray_origin_vec[i]
            axis_direction = ray.direction[i]
            axis_min = self.min_extent[i]
            axis_max = self.max_extent[i]

            if abs(axis_direction) < epsilon:
                # Ray is parallel to the slab planes for this axis
                if axis_origin < axis_min or axis_origin > axis_max:
                    return None # Parallel and outside the slab
            else:
                # Calculate intersection distances with slab planes
                t1 = (axis_min - axis_origin) / axis_direction
                t2 = (axis_max - axis_origin) / axis_direction

                # Ensure t1 is the smaller distance
                if t1 > t2:
                    t1, t2 = t2, t1 # Swap

                # Update overall tmin and tmax
                tmin = max(tmin, t1)
                tmax = min(tmax, t2)

                # Early exit check: if interval becomes invalid
                if tmin >= tmax:
                    return None

        # After checking all axes, if tmin >= tmax, the ray misses the cube.
        if tmin >= tmax:
            return None

        # Determine the correct intersection distance to return.
        # We want the first intersection point *in front* of the ray origin (t > epsilon).
        if tmin > epsilon:
            return tmin  # tmin is the first valid intersection point in front.
        # elif tmax > epsilon: # This case handles when the ray starts inside (tmin <= epsilon < tmax)
            # If we wanted the *exit* point when starting inside, we'd return tmax here.
            # However, the requirement is to return tmin only if tmin > epsilon.
            # Therefore, if tmin <= epsilon, we return None, regardless of tmax.
        #    return tmax # Uncomment this line and comment the 'return None' below it if exit point is desired.
        #    return None
        else:
            # Both tmin and tmax are <= epsilon (or tmin <= epsilon and tmax is irrelevant based on above logic)
            # This means the first intersection is behind or too close to the origin.
            return None


    def normal(self, surface_point):
        """
        Returns the surface normal vector at a given point on the cube's surface.

        Args:
            surface_point: The point on the cube's surface (Point).

        Returns:
            The normal vector (Vector).
        """
        epsilon = 1e-6
        p_vec = surface_point - self.center # Vector from center to surface point

        # Find the component with the largest absolute value
        abs_x = abs(p_vec.x)
        abs_y = abs(p_vec.y)
        abs_z = abs(p_vec.z)

        if abs_x >= abs_y - epsilon and abs_x >= abs_z - epsilon: # Check x-face (allow for tolerance)
            # On x-face, closer to max_extent.x or min_extent.x?
            if p_vec.x > 0:
                return Vector(1, 0, 0)
            else:
                return Vector(-1, 0, 0)
        elif abs_y >= abs_x - epsilon and abs_y >= abs_z - epsilon: # Check y-face
             # On y-face
            if p_vec.y > 0:
                return Vector(0, 1, 0)
            else:
                return Vector(0, -1, 0)
        else: # Must be z-face
             # On z-face
            if p_vec.z > 0:
                return Vector(0, 0, 1)
            else:
                return Vector(0, 0, -1) # Corrected z-face normal


# Placeholder for Point/Vector/Material if they are not globally available
# This part would be removed if imports work correctly
# class Point: def __init__(self, x, y, z): self.x, self.y, self.z = x, y, z
# class Vector: def __init__(self, x, y, z): self.x, self.y, self.z = x, y, z; def __sub__(self, other): return Vector(self.x-other.x, self.y-other.y, self.z-other.z); def __add__(self, other): return Vector(self.x+other.x, self.y+other.y, self.z+other.z); def __getitem__(self, i): return [self.x, self.y, self.z][i]
# class Material: pass
# class Ray: def __init__(self, o, d): self.origin=o; self.direction=d; # Simplified Ray for testing

# Example Usage (for testing logic, remove later)
# center = Point(0, 0, 0)
# size = 2.0
# mat = Material()
# cube = Cube(center, size, mat)
# ray_inside = Ray(Point(0,0,0), Vector(1,1,1))
# ray_outside_hit = Ray(Point(-2, 0, 0), Vector(1, 0, 0))
# ray_outside_miss = Ray(Point(-2, 2, 0), Vector(1, 0, 0))
# ray_parallel_miss = Ray(Point(-2, 0, 0), Vector(0, 1, 0))
# ray_parallel_hit = Ray(Point(-2, 0.5, 0.5), Vector(1, 0, 0)) # Parallel but hits
# print("Inside:", cube.intersects(ray_inside)) # Expected: Should handle inside case, maybe return tmax? Task says return None if tmin < eps.
# print("Outside Hit:", cube.intersects(ray_outside_hit)) # Expected: 1.0
# print("Outside Miss:", cube.intersects(ray_outside_miss)) # Expected: None
# print("Parallel Miss:", cube.intersects(ray_parallel_miss)) # Expected: None
# print("Parallel Hit:", cube.intersects(ray_parallel_hit)) # Expected: 1.0
# surface_point = Point(1, 0.5, 0.5) # On +x face
# print("Normal at", surface_point, ":", cube.normal(surface_point)) # Expected: Vector(1, 0, 0)
# surface_point_neg_z = Point(0.5, 0.5, -1) # On -z face
# print("Normal at", surface_point_neg_z, ":", cube.normal(surface_point_neg_z)) # Expected: Vector(0, 0, -1)

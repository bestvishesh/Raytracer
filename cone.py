import math
from point import Point
from vector import Vector
from material import Material

class Cone:
    """Represents a Y-axis aligned cone."""

    def __init__(self, apex: Point, base_center: Point, base_radius: float, material: Material):
        """
        Initializes the Cone.

        Args:
            apex: The apex point of the cone (Point).
            base_center: The center point of the base cap (Point).
            base_radius: The radius of the base cap (float).
            material: The material of the cone.

        Raises:
            ValueError: If the cone is not Y-axis aligned (apex and base_center have different x or z).
            ValueError: If base_radius is not positive.
            ValueError: If apex and base_center have the same y-coordinate (zero height).
        """
        epsilon = 1e-6 # Define epsilon for checks

        # Ensure axis-aligned
        if abs(apex.x - base_center.x) > epsilon or abs(apex.z - base_center.z) > epsilon:
            raise ValueError("Cone must be aligned with the Y-axis (apex and base_center must have same x and z).")

        # Ensure positive radius
        if base_radius <= epsilon:
             raise ValueError("Cone base_radius must be positive.")

        self.apex = apex
        self.base_center = base_center
        self.base_radius = base_radius
        self.material = material

        # Calculate height and check if positive
        self.height = abs(apex.y - base_center.y)
        if self.height <= epsilon:
            raise ValueError("Cone height must be positive (apex and base_center cannot have the same y-coordinate).")

        # Calculate slope squared (using positive height)
        self.slope_sq = (self.base_radius / self.height) ** 2

        # Store y-bounds and base y-coordinate
        self.min_y = min(apex.y, base_center.y)
        self.max_y = max(apex.y, base_center.y)
        self.base_y = base_center.y


    # Helper function defined within the class scope (as an instance method)
    def check_cap(self, ray, t):
        """Checks if the intersection point at distance t lies within the base cap radius."""
        p = ray.origin + ray.direction * t
        dx = p.x - self.base_center.x
        dz = p.z - self.base_center.z
        # Check if distance squared from center is less than or equal to radius squared
        return (dx*dx + dz*dz) <= self.base_radius**2


    def intersects(self, ray):
        """
        Checks if the ray intersects with the cone (body or base cap).

        Args:
            ray: The ray to check intersection with.

        Returns:
            The distance t to the first intersection point if the ray intersects the cone,
            otherwise None.
        """
        epsilon = 1e-6
        valid_t_cap = float('inf') # Store potential valid cap intersection distance

        # --- Intersection with Base Cap Plane ---
        if abs(ray.direction.y) > epsilon: # Check if ray is not parallel to the base plane
            t_plane = (self.base_y - ray.origin.y) / ray.direction.y
            if t_plane > epsilon: # Intersection must be in front of the ray
                # Check if the hit point is within the radius using the helper
                if self.check_cap(ray, t_plane):
                    valid_t_cap = t_plane # Store valid cap intersection distance


        # --- Intersection with Cone Body (Infinite Cone) ---
        t0, t1 = float('inf'), float('inf') # Initialize potential body intersections

        # Transform ray origin relative to the apex
        co = ray.origin - self.apex
        d = ray.direction

        # Coefficients for the quadratic equation At^2 + Bt + C = 0
        k = self.slope_sq
        A = d.x**2 + d.z**2 - k * d.y**2
        B = 2 * (co.x * d.x + co.z * d.z - k * co.y * d.y)
        C = co.x**2 + co.z**2 - k * co.y**2

        # Handle potential division by zero if A is close to zero
        if abs(A) < epsilon:
            # Solve linear equation B*t + C = 0
            if abs(B) > epsilon:
                t_linear = -C / B
                if t_linear > epsilon:
                    # Store as t0, validity check happens later
                    t0 = t_linear
            # If B is also close to zero, ray is parallel to cone side, no single intersection.
        else:
            # Solve the quadratic equation At^2 + Bt + C = 0
            delta = B*B - 4*A*C
            if delta >= 0: # Real solutions exist (delta == 0 means one solution)
                sqrt_delta = math.sqrt(delta)
                t_sol0 = (-B - sqrt_delta) / (2*A)
                t_sol1 = (-B + sqrt_delta) / (2*A)

                # Ensure t0 <= t1 and store potential solutions
                if t_sol0 <= t_sol1:
                    t0 = t_sol0
                    t1 = t_sol1
                else:
                    t0 = t_sol1
                    t1 = t_sol0


        # --- Check Validity and Find Minimum Intersection (Sequential Update) ---
        min_t = float('inf') # Initialize minimum valid t

        # Check t0 validity
        if t0 != float('inf'): # Check if t0 holds a potential value
             if t0 > epsilon:
                 y0 = ray.origin.y + t0 * ray.direction.y
                 # Check y-bounds exactly as per instruction
                 if self.min_y < y0 < self.max_y:
                     min_t = min(min_t, t0)

        # Check t1 validity
        if t1 != float('inf'): # Check if t1 holds a potential value
            if t1 > epsilon:
                y1 = ray.origin.y + t1 * ray.direction.y
                # Check y-bounds exactly as per instruction
                if self.min_y < y1 < self.max_y:
                    min_t = min(min_t, t1)

        # Check t_cap validity (valid_t_cap already checked for > epsilon and cap bounds)
        if valid_t_cap != float('inf'):
             min_t = min(min_t, valid_t_cap)


        # --- Return result ---
        if min_t == float('inf'):
            return None # No valid intersection found
        else:
            return min_t


    def normal(self, surface_point):
        """
        Returns the surface normal vector at a given point on the cone's surface.

        Args:
            surface_point: The point on the cone's surface (Point).

        Returns:
            The normalized normal vector (Vector).
        """
        epsilon = 1e-6

        # --- Check if on Base Cap ---
        if abs(surface_point.y - self.base_y) < epsilon:
            # If apex is above base (cone pointing down), base normal is (0, 1, 0).
            if self.apex.y > self.base_y:
                return Vector(0, 1, 0)   # Base faces up
            # If apex is below base (cone pointing up), base normal is (0, -1, 0).
            else:
                return Vector(0, -1, 0)  # Base faces down


        # --- Calculate Normal for Slanted Surface ---
        else:
            # Vector from apex to surface point
            v = surface_point - self.apex

            # Calculate magnitude of projection onto xz-plane
            # Check if m is close to zero (point is near apex)
            m_sq = v.x**2 + v.z**2
            if m_sq < epsilon:
                 # Point is very close to the apex, normal is undefined.
                 # Return a fallback normal pointing along the axis, away from the base.
                 if self.apex.y > self.base_y: # Cone points down
                    return Vector(0, 1, 0) # Normal points up from apex
                 else: # Cone points up
                    return Vector(0, -1, 0) # Normal points down from apex

            m = math.sqrt(m_sq)

            # Calculate the y-component of the normal based on slope and orientation.
            y_diff = self.apex.y - self.base_center.y
            # Use math.copysign to get the sign of y_diff
            ny_sign = math.copysign(1.0, y_diff) # Use 1.0 to ensure float result
            ny = m * math.sqrt(self.slope_sq) * ny_sign

            # Construct the normal vector: (v.x, ny, v.z)
            normal_vec = Vector(v.x, ny, v.z)

            # Return the normalized normal vector
            return normal_vec.normalize()

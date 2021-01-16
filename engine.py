from image import Image
from ray import Ray
from point import Point
from color import Color


class RenderEngine:
    """Renders 3D objects as 2D objects using Raytracing"""
    MAX_DEPTH = 6
    MIN_DISPLACE = 0.00001

    def render(self, scene):
        width = scene.width
        height = scene.height
        aspect_ratio = float(width)/height
        x0 = -1.0
        x1 = 1.0
        xstep = (x1-x0)/(width-1)
        y0 = -1.0/aspect_ratio
        y1 = 1.0/aspect_ratio
        ystep = (y1-y0)/(height-1)

        camera = scene.camera
        pixels = Image(width, height)

        for j in range(height):
            y = y0 + j*ystep
            for i in range(width):
                x = x0 + i*xstep
                ray = Ray(camera, Point(x, y) - camera)
                pixels.set_pixel(i, j, self.ray_trace(ray, scene))
            print("{:3.0f}%".format(float(j)*100/float(height)), end="\r")
        return pixels

    def ray_trace(self, ray, scene, depth=0):
        color = Color(0, 0, 0)
        # Find the nearest object that the ray hits.
        hit_dist, hit_obj = self.find_nearest(ray, scene)
        if hit_obj is None:
            return color
        hit_pos = ray.origin + ray.direction*hit_dist
        hit_normal = hit_obj.normal(hit_pos)
        color += self.color_at(hit_obj, hit_pos, hit_normal, scene)
        if depth < self.MAX_DEPTH:
            new_ray_pos = hit_pos + hit_normal*self.MIN_DISPLACE
            new_ray_dir = ray.direction - 2*ray.direction.dot_product(hit_normal)*hit_normal
            new_ray = Ray(new_ray_pos,new_ray_dir)
            # Attentuate the Reflected ray by the reflection coffecient
            color += self.ray_trace(new_ray, scene, depth+1) * hit_obj.material.reflection 
        return color

    def find_nearest(self, ray, scene):
        min_dist = None
        hit_obj = None
        for obj in scene.objects:
            dist = obj.intersects(ray)
            if dist is not None and (hit_obj is None or min_dist > dist):
                min_dist = dist
                hit_obj = obj
        return (min_dist, hit_obj)

    def color_at(self, hit_obj, hit_pos, normal, scene):
        material = hit_obj.material
        obj_color = material.color_at(hit_pos)
        to_cam = scene.camera - hit_pos
        specular_k = 50
        color = material.ambient * Color.from_hex("#FFFFFF")

        # Light calculations
        for light in scene.lights:
            to_light = Ray(hit_pos, light.position - hit_pos)
            # Diffuse shading (Lambert)
            color += obj_color * material.diffuse * \
                max(normal.dot_product(to_light.direction), 0)
            # Specular shading (Phong Blinn)
            half_vector = (to_light.direction + to_cam).normalize()
            color += light.color * material.specular * \
                max(normal.dot_product(half_vector), 0) ** specular_k
        return color

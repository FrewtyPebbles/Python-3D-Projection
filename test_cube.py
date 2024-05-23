from PIL import Image, ImageDraw
import time
from camera import Screen, Camera
from mesh import Mesh, Polygon
from object import Object
from vertex import Vec3
import math as m

# Use PIL as render medium
img = Image.new("RGB", (500,500))
background = Image.open("./assets\space.jpg").resize((500,500))
img_draw = ImageDraw.Draw(img)

# Create Screen and Camera
screen = Screen(img.width, img.height)
camera = Camera(Vec3(0.0,0.0,0.0), img.width, img.height, 200)

# render functions

def wire_render_func(pos_1:Vec3, pos_2:Vec3):
    "Wireframe render function"
    (x1, y1),(x2, y2)= pos_1.project(camera, screen), pos_2.project(camera, screen)
    img_draw.line((x1, y1, x2, y2), "black", 0)


def render_func(polygon:Polygon):
    "Polygon render function"
    (min_x, min_y), (max_x, max_y) = polygon.get_projection_rect(camera, screen)
    avg_d_norm = sum([vec3.get_normalized().z * 255 for vec3 in polygon.connections])/len(polygon.connections)
    shade = 255-int(avg_d_norm)

    avg_d = sum([vec3.z for vec3 in polygon.connections])/len(polygon.connections)

    for y in range(int(min_y), int(max_y)):
        for x in range(int(min_x), int(max_x)):
            if (camera.depth_buffer[x][y] > avg_d) \
            if camera.depth_buffer[x][y] != None else True:
                if polygon.in_projection(x,y, camera, screen):
                    img_draw.point((x,y), (shade, shade, shade, 255))
                    camera.depth_buffer[x][y] = avg_d

# Load the mesh/create the 3D object
t1 = time.time()
scale = 20
cube = Object(Mesh(
    [
        Vec3(-scale,-scale,-scale),
        Vec3( scale,-scale,-scale),
        Vec3( scale-10, scale-10,10-scale),
        Vec3(-scale, scale,-scale),
        Vec3(-scale,-scale, scale),
        Vec3( scale,-scale, scale),
        Vec3( scale, scale, scale),
        Vec3(-scale, scale, scale)
    ],
    [
        [0,1,2,3],
        [4,5,6,7],
        [0,1,5,4],
        [1,2,6,5],
        [0,3,7,4],
        [2,3,7,6],
    ]
), Vec3(0, 0, 60))
t2 = time.time()
print(f"time to load mesh: {(t2-t1)*1000}")

# Record the animation frames
frames = []
t1 = time.time()

img.paste(background)
camera.render([cube], render_func)
img_draw.text((0,0), "DENTED CUBE ROTATE")
frames.append(img.copy())

for _ in range(60):
    img.paste(background)
    cube.rotation += 0.2
    rt1 = time.time()
    camera.render([cube], render_func)
    rt2 = time.time()
    print(f"\tframe render time: {(rt2-rt1)*1000} ms")
    img_draw.text((0,0), "DENTED CUBE ROTATE")
    frames.append(img.copy())

t2 = time.time()
print(f"time to render: {(t2-t1)*1000} ms")

# Save to render medium
img.save("result.gif", save_all = True, append_images = frames, duration = 3, loop = 0)
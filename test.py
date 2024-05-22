from PIL import Image, ImageDraw
import time
from camera import Screen, Camera
from mesh import Mesh
from object import Object
from vertex import Vec3

#img = Image.new("RGB", (500,500), "white")
img = Image.open("./assets/space.jpg")
img_draw = ImageDraw.Draw(img)
screen = Screen(img.width, img.height)
camera = Camera(Vec3(0.0,0.0,0.0), img.width, img.height, 200)
# cube = Mesh(
#     [
#         #front face
#         Vec3(-1, -1, -1), #0 LD
#         Vec3(-1,  1, -1), #1 LU
#         Vec3(1, 1, -1),   #2 RU
#         Vec3(1, -1, -1),  #3 RD
#         #back face
#         Vec3(-1, -1, 1),  #4 LD
#         Vec3(-1,  1, 1),  #5 LU
#         Vec3(1,  1, 1),   #6 RU
#         Vec3(1, -1, 1),   #7 RD
#     ],
#     [
#         # FRONT
#         [0,1,2],
#         [2,3,0],
#         # SIDES
#         [0,4,5],
#         [1,5,6],
#         [2,6,7],
#         [3,7,4],
#         # BACK
#         [4,5,6],
#         [6,7,4]
#     ]
# )

half_w = img.width/2
half_h = img.height/2

def render_func(pos_1:Vec3, pos_2:Vec3):
    (x1, y1),(x2, y2)= pos_1.project(camera, screen), pos_2.project(camera, screen)
    img_draw.line((half_w+x1, half_h+y1, half_w+x2, half_h+y2), "white", 0)


teapot = Object(Mesh.from_file("./meshes/teapot.obj"))
#cube_obj = Object(cube)

teapot.position.z = 100
teapot.position.y = -50
t1 = time.time()
teapot.render(render_func)
t2 = time.time()
print(f"time to render: {(t2-t1)*1000}")

img.save("result.png")
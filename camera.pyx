from __future__ import annotations
from typing import Callable
from mesh import Polygon
from object import Object
import math as m

cdef class Screen:
    def __init__(self, width:int, height:int) -> None:
        self.width = width
        self.height = height
    
cdef class Camera:
    def __init__(self, Vec3 position, int view_width, int view_height, int view_distance) -> None:
        self.position = position
        self.view_width = view_width
        self.view_height = view_height
        self.view_distance = view_distance
        self.depth_buffer = [[m.inf for _ in range(view_height)] for _ in range(view_width)]

    def clear_depth_buffer(self):
        self.depth_buffer = [[m.inf for _ in range(self.view_height)] for _ in range(self.view_width)]

    def render(self, objects:list[Object],
        render_function:Callable[[Polygon],None] | None = None,
        wire_render_func:Callable[[Vec3, Vec3],None] | None = None):
        for obj in objects:
            obj.render(render_function, wire_render_func)
            
        self.clear_depth_buffer()
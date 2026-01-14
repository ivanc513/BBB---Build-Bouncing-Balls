import numpy as np
import pygame
from OpenGL.GL import *
import math
import random
from OpenGL import *
from .base_object import SimObject

RED = (255, 0, 0)

class Ball(SimObject):
    def __init__(self, pos, vel, radius=5, color=(1.0,0.0,0.0), sfx=None):
        super().__init__(pos)
        self.v = np.array(vel, dtype=np.float32)
        self.radius = radius
        self.color = np.array(color, dtype=np.float32)
        self.sfx = sfx

        self.is_in = True

    @property
    def is_dynamic(self):
        return True

    def update(self, dt, world):
        self.pos += self.v * dt

    def on_collision(self, other, world):
        pass

    def draw(self):
        glColor3f(*self.color)  # RGB in 0-1 range
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(*self.pos)  # center of circle
        num_segments = 20 
        for i in range(num_segments + 1):
            theta = 2.0 * math.pi * i / num_segments
            x = self.pos[0] + self.radius * math.cos(theta)
            y = self.pos[1] + self.radius * math.sin(theta)
            glVertex2f(x, y)
        glEnd()

    @staticmethod
    def is_in_arc(point, center, start_angle, end_angle):
        dx = point[0] - center[0]
        dy = point[1] - center[1]
        angle = math.atan2(dy, dx) % (2 * math.pi)
        start = start_angle % (2 * math.pi)
        end = end_angle % (2 * math.pi)

        if start <= end:
           return start <= angle <= end
        else:
            return angle >= start or angle <= end
        

import numpy as np
import pygame
from OpenGL.GL import *
import math
import random
from OpenGL import *
from .base_object import SimObject

RED = (255, 0, 0)

class Ball(SimObject):
    def __init__(self, pos, vel, radius=5, color=(1.0,0.0,0.0), sfx=None, vfx=None):
        super().__init__(pos)
        self.v = np.array(vel, dtype=np.float32)
        self.radius = radius
        self.color = np.array(color, dtype=np.float32)
        self.sfx = sfx
        self.vfx = vfx

        self.is_in = True
        self.trail = []
        self.trail_length = 10

    @property
    def is_dynamic(self):
        return True

    def update(self, dt, world):
        new_pos = self.pos + self.v * dt

        if self.vfx == "trailing_motion":
            if len(self.trail) > 0:
                last_pos = self.trail[-1]
                steps = int(np.linalg.norm(new_pos - last_pos) / 2)  # 2 pixels per step
                for s in range(1, steps + 1):
                    interp = last_pos + (new_pos - last_pos) * (s / steps)
                    self.trail.append(interp)
            else:
                self.trail.append(np.copy(new_pos))

            # Keep trail length in check
            if len(self.trail) > self.trail_length:
                self.trail = self.trail[-self.trail_length:]

        # Update position
        self.pos = new_pos

    def on_collision(self, other, world):
        pass

    def draw(self):
        if self.vfx == "trailing_motion" and len(self.trail) > 0:
            n = len(self.trail)
            for i, p in enumerate(self.trail):
                t = i / n  # 0 = oldest, 1 = newest
                alpha = t**2 * 0.3  # older points fade faster
                glColor4f(self.color[0], self.color[1], self.color[2], alpha)

                glBegin(GL_TRIANGLE_FAN)
                glVertex2f(p[0], p[1])  # center of trail circle
                num_segments = max(20, int(self.radius * (0.5 + t) * 2))
                for j in range(num_segments + 1):
                    theta = 2.0 * math.pi * j / num_segments
                    x = p[0] + self.radius * (0.5 + t) * math.cos(theta)
                    y = p[1] + self.radius * (0.5 + t) * math.sin(theta)
                    glVertex2f(x, y)
                glEnd()

        # Draw current ball
        glColor4f(self.color[0], self.color[1], self.color[2], 1.0)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(self.pos[0], self.pos[1])  # center of ball
        num_segments = max(20, int(self.radius * 2))
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
        

import numpy as np
import pygame
import math

class Ball:
    def __init__(self, pos, vel, radius=5, color=(255, 0, 0)):
        self.pos = np.array(pos, dtype=np.float64)
        self.v = np.array(vel, dtype=np.float64)
        self.radius = radius
        self.color = color
        self.is_in = True

    def update(self, gravity):
        self.v[1] += gravity
        self.pos += self.v

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos.astype(int), self.radius)

    @staticmethod
    def is_in_arc(point, center, start_angle, end_angle):
        dx = point[0] - center[0]
        dy = point[1] - center[1]
        ball_angle = math.atan2(dy,dx)
        end_angle = end_angle % (2 * math.pi)
        start_angle = start_angle % (2 * math.pi)
        if start_angle >= end_angle:
            end_angle += 2 * math.pi
        if start_angle <= ball_angle <= end_angle or (start_angle <= ball_angle + 2 * math.pi <= end_angle):
            return True

        
        '''
        v = point - center
        angle = math.atan2(v[1], v[0])

        # normalize angle to [0, 2π)
        angle = (angle + 2 * math.pi) % (2 * math.pi)
        start = (start_angle + 2 * math.pi) % (2 * math.pi)
        end = (end_angle + 2 * math.pi) % (2 * math.pi)

        if start < end:
            return start <= angle <= end
        return angle >= start or angle <= end
        '''

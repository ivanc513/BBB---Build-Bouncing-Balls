from OpenGL.GL import *
from core.objects.ball import Ball
from core.conditions.ball_count import BallCount
import random

class World:
    def __init__(self, arena, width, height, constraints, end_condition):
        self.arena = arena
        self.width = width
        self.height = height
        self.constraints = constraints
        self.end_condition = end_condition

        self.objects = [arena]
        self.running = True

    def spawn(self, obj):
        self.objects.append(obj)

    def on_destroy(self, obj):
        if isinstance(self.end_condition, BallCount):
            for _ in range(2):
                self.spawn(
                Ball(
                    pos=[self.width / 2, self.height / 2 - 120],
                    vel=[random.uniform(-4, 4), random.uniform(-1, 1)],
                    radius=obj.radius
                )
            )

    def update(self, dt):
        alive_objects = []

        for obj in self.objects:
            for constraint in self.constraints:
                constraint.apply(obj, dt, self)

        for obj in self.objects:
            obj.update(dt, self)

        for obj in self.objects:
            for other in self.objects:
                if obj is not other:
                    other.on_collision(obj, self)

            if self.is_out_of_bounds(obj):
                self.on_destroy(obj)
            else:
                alive_objects.append(obj)

        self.objects = alive_objects

        if self.end_condition.is_met(self):
            self.running = False
        return

    def is_out_of_bounds(self, obj):
        x, y = obj.pos
        return (
            x < 0 or x > self.width or
            y < 0 or y > self.height
        )
    
    def draw(self):
        self.arena.draw()
        for obj in self.objects:
            obj.draw()

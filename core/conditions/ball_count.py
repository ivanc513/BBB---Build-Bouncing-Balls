from .base_condition import EndCondition
from ..objects.ball import Ball

class BallCount(EndCondition):
    def __init__(self, target):
        self.target = target

    def is_met(self, world):
        count = sum(isinstance(obj, Ball) for obj in world.objects)
        return count >= self.target
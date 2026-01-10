from .base_constraints import Constraint

class Gravity(Constraint):
    def __init__(self, g):
        self.g = g

    def apply(self, obj, dt, world):
        if not getattr(obj, "is_dynamic", False):
            return
        obj.v[1] += self.g * dt
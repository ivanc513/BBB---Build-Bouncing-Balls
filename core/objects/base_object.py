import numpy as np

class SimObject:
    def __init__(self, position):
        self.pos = np.array(position, dtype=np.float64)

    def update(self, dt, world):
        pass

    def draw(self, surface):
        pass

    @property
    def is_dynamic(self):
        return False
    
    def on_collision(self, other, world):
        pass

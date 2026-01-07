from core.ball import Ball

class World:
    def __init__(self, arena, width, height, gravity):
        self.arena = arena
        self.width = width
        self.height = height
        self.gravity = gravity

        self.objects = [arena]
        self.running = True

    def spawn(self, obj):
        self.objects.append(obj)

    def update(self, dt):
        alive_objects = []

        for obj in self.objects:
            obj.update(dt, self)
            
        for obj in self.objects:
            for other in self.objects:
                if obj is not other:
                    other.on_collision(obj, self)

            if self.is_out_of_bounds(obj):
                obj.on_destroy(self)
            else:
                alive_objects.append(obj)

        self.objects = alive_objects

    def is_out_of_bounds(self, obj):
        x, y = obj.pos
        return (
            x < 0 or x > self.width or
            y < 0 or y > self.height
        )
    
    def draw(self, surface):
        self.arena.draw(surface)
        for obj in self.objects:
            obj.draw(surface)

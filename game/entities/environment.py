
from game.utils.geometry_factory import GeometryFactory

class Environment:
    def __init__(self, base):
        self.base = base
        self.root = self.base.render.attachNewNode("environment")

        self.create_kitchen_floor()
        self.create_dining_floor()
        self.create_walls()

    def create_kitchen_floor(self):
        # Kitchen floor: Checkered tile look
        floor_root = self.root.attachNewNode("kitchen_floor")
        for x in range(-8, 8, 2):
            for y in range(0, 10, 2):
                color = (0.9, 0.9, 0.9, 1) if (x+y)%4 == 0 else (0.7, 0.7, 0.7, 1)
                GeometryFactory.create_box(self.base.loader, floor_root, pos=(x, y, -0.05), scale=(2, 2, 0.1), color=color)

    def create_dining_floor(self):
        # Dining floor: Wooden look
        GeometryFactory.create_box(self.base.loader, self.root, pos=(0, -8, -0.05), scale=(20, 16, 0.1), color=(0.4, 0.25, 0.15, 1))
        # Divider/Transition
        GeometryFactory.create_box(self.base.loader, self.root, pos=(0, 0, -0.02), scale=(20, 0.5, 0.1), color=(0.2, 0.1, 0.05, 1))

    def create_walls(self):
        # Back wall
        GeometryFactory.create_box(self.base.loader, self.root, pos=(0, 10, 2), scale=(20, 0.5, 4), color=(0.8, 0.8, 0.7, 1))
        # Side walls
        GeometryFactory.create_box(self.base.loader, self.root, pos=(-10, 0, 2), scale=(0.5, 20, 4), color=(0.8, 0.8, 0.7, 1))
        GeometryFactory.create_box(self.base.loader, self.root, pos=(10, 0, 2), scale=(0.5, 20, 4), color=(0.8, 0.8, 0.7, 1))

        # Add some baseboards
        GeometryFactory.create_box(self.base.loader, self.root, pos=(0, 9.7, 0.2), scale=(20, 0.1, 0.4), color=(0.4, 0.2, 0.1, 1))

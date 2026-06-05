
from panda3d.core import Vec3, NodePath
from game.utils.geometry_factory import GeometryFactory

class Item:
    def __init__(self, base, name, state="raw"):
        self.base = base
        self.name = name
        self.state = state
        self.contents = [] # For plates

        self.model = self.base.render.attachNewNode(f"item_{name}")
        self.visual_node = self.model.attachNewNode("visual")

        self.create_visual()

    def create_visual(self):
        self.visual_node.getChildren().detach()

        if self.name == "Plate":
            # Plate is a flat white cylinder-like box
            GeometryFactory.create_box(self.base.loader, self.visual_node, scale=(0.8, 0.8, 0.05), color=(0.95, 0.95, 0.95, 1))
            # Rim
            GeometryFactory.create_box(self.base.loader, self.visual_node, pos=(0,0,0.02), scale=(0.85, 0.85, 0.02), color=(0.9, 0.9, 0.9, 1))

        elif self.name == "Tomato":
            if self.state == "raw":
                # Red sphere
                GeometryFactory.create_sphere(self.base.loader, self.visual_node, scale=0.4, color=(0.9, 0.1, 0.1, 1))
                # Green stem
                GeometryFactory.create_box(self.base.loader, self.visual_node, pos=(0,0,0.35), scale=(0.1, 0.1, 0.1), color=(0.1, 0.6, 0.1, 1))
            elif self.state == "cut":
                # Slice
                GeometryFactory.create_box(self.base.loader, self.visual_node, scale=(0.4, 0.4, 0.1), color=(0.8, 0, 0, 1))

        elif self.name == "Onion":
            if self.state == "raw":
                GeometryFactory.create_sphere(self.base.loader, self.visual_node, scale=0.35, color=(1, 0.9, 0.7, 1))
                GeometryFactory.create_box(self.base.loader, self.visual_node, pos=(0,0,0.3), scale=(0.05, 0.05, 0.15), color=(0.5, 0.4, 0.2, 1))
            elif self.state == "cut":
                GeometryFactory.create_box(self.base.loader, self.visual_node, scale=(0.35, 0.35, 0.05), color=(1, 1, 1, 1))

        elif self.name == "Meat": # Adding meat as per screenshots
            if self.state == "raw":
                # Red meat part
                GeometryFactory.create_box(self.base.loader, self.visual_node, scale=(0.5, 0.4, 0.15), color=(0.8, 0.2, 0.2, 1))
                # Bone part
                GeometryFactory.create_sphere(self.base.loader, self.visual_node, pos=(0.2, 0.15, 0), scale=0.15, color=(0.95, 0.95, 0.95, 1))
            elif self.state == "cut":
                GeometryFactory.create_box(self.base.loader, self.visual_node, scale=(0.4, 0.3, 0.1), color=(0.7, 0.1, 0.1, 1))
            elif self.state == "cooked":
                GeometryFactory.create_box(self.base.loader, self.visual_node, scale=(0.4, 0.3, 0.1), color=(0.4, 0.2, 0.1, 1))

        elif self.name == "extinguisher":
            GeometryFactory.create_box(self.base.loader, self.visual_node, scale=(0.2, 0.2, 0.6), color=(0.8, 0.1, 0.1, 1))
            GeometryFactory.create_box(self.base.loader, self.visual_node, pos=(0, 0.15, 0.25), scale=(0.05, 0.2, 0.05), color=(0.1, 0.1, 0.1, 1))

        if self.state == "burnt":
            for child in self.visual_node.getChildren():
                child.setColor(0.1, 0.1, 0.1, 1)

    def update_visual(self):
        self.create_visual()

    def destroy(self):
        self.model.removeNode()

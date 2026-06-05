
from panda3d.core import Vec3

class Item:
    def __init__(self, base, name, state="raw"):
        self.base = base
        self.name = name
        self.state = state

        # Visual
        self.model = self.base.loader.loadModel("models/smiley")
        self.model.setScale(0.3)
        self.model.reparentTo(self.base.render)

        # Color based on state
        self.update_visual()

    def update_visual(self):
        if self.state == "raw":
            self.model.setColor(1, 1, 1, 1)
        elif self.state == "cut":
            self.model.setColor(0.5, 1, 0.5, 1)
        elif self.state == "cooked":
            self.model.setColor(1, 0.5, 0, 1)
        elif self.state == "burnt":
            self.model.setColor(0.2, 0.2, 0.2, 1)

    def destroy(self):
        self.model.removeNode()

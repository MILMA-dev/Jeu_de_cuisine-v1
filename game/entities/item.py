
from panda3d.core import Vec3

class Item:
    def __init__(self, base, name, state="raw"):
        self.base = base
        self.name = name
        self.state = state
        self.contents = [] # For plates

        # Visual
        if self.name == "Plate":
            self.model = self.base.loader.loadModel("models/box")
            self.model.setScale(0.5, 0.5, 0.05)
        elif self.name == "extinguisher":
            self.model = self.base.loader.loadModel("models/box")
            self.model.setScale(0.2, 0.2, 0.6)
        else:
            self.model = self.base.loader.loadModel("models/smiley")
            self.model.setScale(0.3)

        self.model.reparentTo(self.base.render)

        # Color based on state
        self.update_visual()

    def update_visual(self):
        if self.name == "Tomato":
            if self.state == "raw": self.model.setColor(1, 0, 0, 1)
            elif self.state == "cut": self.model.setColor(0.8, 0, 0, 1); self.model.setScale(0.3, 0.3, 0.1)
            elif self.state == "cooked": self.model.setColor(0.6, 0.2, 0, 1)
        elif self.name == "Onion":
            if self.state == "raw": self.model.setColor(1, 0.9, 0.8, 1)
            elif self.state == "cut": self.model.setColor(1, 1, 1, 1); self.model.setScale(0.3, 0.3, 0.05)
            elif self.state == "cooked": self.model.setColor(0.8, 0.6, 0.4, 1)

        if self.state == "burnt":
            self.model.setColor(0.1, 0.1, 0.1, 1)

    def destroy(self):
        self.model.removeNode()

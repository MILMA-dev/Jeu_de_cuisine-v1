
from panda3d.core import NodePath, CardMaker, BillboardEffect

class ProgressBar:
    def __init__(self, parent, pos=(0, 0, 1.5)):
        self.container = parent.attachNewNode("progress_container")
        self.container.setPos(pos)
        self.container.setBillboardPointEye()

        cm = CardMaker("bar")
        cm.setFrame(-0.5, 0.5, -0.05, 0.05)

        self.background = self.container.attachNewNode(cm.generate())
        self.background.setColor(0.2, 0.2, 0.2, 1)

        self.foreground = self.container.attachNewNode(cm.generate())
        self.foreground.setColor(0, 1, 0, 1)
        self.foreground.setZ(0.001) # Slightly in front

        self.container.hide()

    def set_progress(self, ratio):
        if ratio <= 0:
            self.container.hide()
        else:
            self.container.show()
            self.foreground.setScale(ratio, 1, 1)
            # Offset to scale from left
            self.foreground.setX(-0.5 * (1 - ratio))

    def set_color(self, r, g, b, a=1):
        self.foreground.setColor(r, g, b, a)

    def destroy(self):
        self.container.removeNode()

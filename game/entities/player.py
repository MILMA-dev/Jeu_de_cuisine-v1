
from panda3d.core import Vec3

class Player:
    def __init__(self, base, input_manager):
        self.base = base
        self.input_manager = input_manager

        # Player visual (Composition)
        self.model = self.base.render.attachNewNode("player_root")

        # Body
        self.body = self.base.loader.loadModel("models/box")
        self.body.reparentTo(self.model)
        self.body.setScale(0.6, 0.4, 0.8)
        self.body.setZ(0.4)
        self.body.setColor(0.2, 0.4, 0.8, 1)

        # Head
        self.head = self.base.loader.loadModel("models/smiley")
        self.head.reparentTo(self.model)
        self.head.setZ(1.1)
        self.head.setScale(0.25)

        # Chef hat (simple white box)
        self.hat = self.base.loader.loadModel("models/box")
        self.hat.reparentTo(self.model)
        self.hat.setZ(1.4)
        self.hat.setScale(0.2, 0.2, 0.3)
        self.hat.setColor(1, 1, 1, 1)

        self.model.setPos(0, 0, 0)

        self.speed = 10.0
        self.held_item = None

        # Movement vector
        self.move_vec = Vec3(0, 0, 0)

    def update(self, dt):
        self.move_vec.set(0, 0, 0)

        if self.input_manager.is_pressed("up"):
            self.move_vec.setY(1)
        if self.input_manager.is_pressed("down"):
            self.move_vec.setY(-1)
        if self.input_manager.is_pressed("left"):
            self.move_vec.setX(-1)
        if self.input_manager.is_pressed("right"):
            self.move_vec.setX(1)

        if self.move_vec.length() > 0:
            self.move_vec.normalize()
            self.model.setPos(self.model.getPos() + self.move_vec * self.speed * dt)

        # Keep held item on top of player
        if self.held_item:
            self.held_item.model.setPos(self.model.getPos() + Vec3(0, 0, 1.2))

    def pick_up(self, item):
        if not self.held_item:
            self.held_item = item
            item.model.reparentTo(self.model)
            item.model.setPos(0, 0, 1.2)
            return True
        return False

    def drop(self):
        if self.held_item:
            item = self.held_item
            item.model.reparentTo(self.base.render)
            item.model.setPos(self.model.getPos() + Vec3(0, 1, 0)) # Drop in front
            self.held_item = None
            return item
        return None

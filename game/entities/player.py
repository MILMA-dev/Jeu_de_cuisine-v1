
from panda3d.core import Vec3

class Player:
    def __init__(self, base, input_manager):
        self.base = base
        self.input_manager = input_manager

        # Player visual (a simple box for now)
        self.model = self.base.loader.loadModel("models/box")
        self.model.reparentTo(self.base.render)
        self.model.setScale(0.5, 0.5, 1.0)
        self.model.setPos(0, 0, 0.5)
        self.model.setColor(0, 0.7, 1, 1)

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

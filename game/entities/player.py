
from panda3d.core import Vec3, NodePath
from game.utils.geometry_factory import GeometryFactory

class Player:
    def __init__(self, base, input_manager):
        self.base = base
        self.input_manager = input_manager

        # Player root
        self.model = self.base.render.attachNewNode("player_root")

        # Stylized Body
        # Shoes
        GeometryFactory.create_box(self.base.loader, self.model, pos=(-0.2, 0, 0.1), scale=(0.2, 0.3, 0.2), color=(0.1, 0.1, 0.1, 1))
        GeometryFactory.create_box(self.base.loader, self.model, pos=(0.2, 0, 0.1), scale=(0.2, 0.3, 0.2), color=(0.1, 0.1, 0.1, 1))

        # Pants (Blue)
        GeometryFactory.create_box(self.base.loader, self.model, pos=(0, 0, 0.4), scale=(0.5, 0.3, 0.4), color=(0.2, 0.3, 0.6, 1))

        # Jacket (White)
        GeometryFactory.create_box(self.base.loader, self.model, pos=(0, 0, 0.9), scale=(0.55, 0.35, 0.6), color=(0.95, 0.95, 0.95, 1))
        # Buttons
        for z in [0.8, 1.0]:
            GeometryFactory.create_sphere(self.base.loader, self.model, pos=(0.1, 0.18, z), scale=0.03, color=(0.1, 0.1, 0.1, 1))

        # Head (Peach skin tone)
        self.head = GeometryFactory.create_sphere(self.base.loader, self.model, pos=(0, 0, 1.3), scale=0.3, color=(1, 0.8, 0.7, 1))

        # Hat
        GeometryFactory.create_chef_hat(self.base.loader, self.model, pos=(0, 0, 1.5))

        # Hands/Arms
        self.left_arm = GeometryFactory.create_box(self.base.loader, self.model, pos=(-0.35, 0, 0.9), scale=(0.15, 0.15, 0.4), color=(0.95, 0.95, 0.95, 1))
        self.right_arm = GeometryFactory.create_box(self.base.loader, self.model, pos=(0.35, 0, 0.9), scale=(0.15, 0.15, 0.4), color=(0.95, 0.95, 0.95, 1))

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

            # Rotate to face movement
            target_h = Vec3(0, 1, 0).relativeAngleTo(self.move_vec)
            # Simple rotation fix
            if self.move_vec.getX() < 0:
                 self.model.setH(target_h)
            else:
                 self.model.setH(-target_h)

        # Keep held item in front of player (hands area)
        if self.held_item:
            self.held_item.model.setPos(self.model.getPos() + self.model.getQuat().getForward() * 0.8 + Vec3(0, 0, 1.0))

    def pick_up(self, item):
        if not self.held_item:
            self.held_item = item
            item.model.reparentTo(self.model)
            # Item position relative to player
            item.model.setPos(0, 0.8, 1.0)
            return True
        return False

    def drop(self):
        if self.held_item:
            item = self.held_item
            item.model.reparentTo(self.base.render)
            item.model.setPos(self.model.getPos() + self.model.getQuat().getForward() * 1.0)
            self.held_item = None
            return item
        return None

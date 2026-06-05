
from panda3d.core import Vec3, TextNode
from game.utils.geometry_factory import GeometryFactory
import random

class Customer:
    def __init__(self, base, table):
        self.base = base
        self.table = table

        # Visual
        self.model = self.base.render.attachNewNode("customer_root")

        # Stylized Body
        color = (random.uniform(0.4, 0.9), random.uniform(0.4, 0.9), random.uniform(0.4, 0.9), 1)
        GeometryFactory.create_box(self.base.loader, self.model, pos=(0, 0, 0.5), scale=(0.5, 0.3, 0.8), color=color)
        # Head
        GeometryFactory.create_sphere(self.base.loader, self.model, pos=(0, 0, 1.2), scale=0.3, color=(1, 0.8, 0.7, 1))
        # Hair/Hat
        hair_color = random.choice([(0.2, 0.1, 0), (0.9, 0.8, 0.2), (0.5, 0.5, 0.5)])
        GeometryFactory.create_sphere(self.base.loader, self.model, pos=(0, 0, 1.4), scale=(0.32, 0.32, 0.15), color=hair_color)

        # Start at "door"
        self.model.setPos(12, -8, 0) # Door position
        self.target_pos = table.model.getPos() + Vec3(0, -1.2, 0)
        self.state = "walking_to_table"
        self.speed = 5.0
        self.order = None

        # Order bubble (simple text for now, could be icon)
        self.bubble = self.model.attachNewNode("bubble")
        self.bubble.setPos(0, 0, 2.0)
        self.bubble.setBillboardPointEye()
        self.bubble_text = TextNode('order_bubble')
        self.bubble_text.setText("")
        self.bubble_text.setAlign(TextNode.ACenter)
        self.bubble_node = self.bubble.attachNewNode(self.bubble_text)
        self.bubble_node.setScale(0.4)
        self.bubble_node.hide()

    def update(self, dt):
        if self.state == "walking_to_table":
            diff = self.target_pos - self.model.getPos()
            if diff.length() < 0.2:
                self.state = "waiting_for_order"
                self.table.occupied_by = self
                self.model.setH(180) # Face the table
            else:
                diff.setZ(0)
                diff.normalize()
                self.model.setPos(self.model.getPos() + diff * self.speed * dt)
                # Face movement
                self.model.lookAt(self.model.getPos() + diff)

        elif self.state == "waiting_for_order":
            if self.order:
                self.bubble_node.show()
                self.bubble_text.setText(f"{self.order.recipe_name}\n({int(self.order.time_left)}s)")

        elif self.state == "leaving":
            self.bubble_node.hide()
            target = Vec3(12, -8, 0)
            diff = target - self.model.getPos()
            if diff.length() < 0.2:
                self.destroy()
            else:
                diff.setZ(0)
                diff.normalize()
                self.model.setPos(self.model.getPos() + diff * self.speed * dt)
                self.model.lookAt(self.model.getPos() + diff)

    def leave(self):
        self.state = "leaving"
        if self.table:
            self.table.occupied_by = None

    def destroy(self):
        self.model.removeNode()
        if self in self.base.customers:
            self.base.customers.remove(self)

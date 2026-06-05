
from panda3d.core import NodePath, Vec3, Vec4

class GeometryFactory:
    @staticmethod
    def create_box(loader, parent, pos=(0,0,0), scale=(1,1,1), hpr=(0,0,0), color=(1,1,1,1)):
        model = loader.loadModel("models/box")
        model.reparentTo(parent)
        model.setPos(pos)
        model.setScale(scale)
        model.setHpr(hpr)
        model.setColor(color)
        return model

    @staticmethod
    def create_sphere(loader, parent, pos=(0,0,0), scale=(1,1,1), hpr=(0,0,0), color=(1,1,1,1)):
        model = loader.loadModel("models/smiley")
        model.reparentTo(parent)
        model.setPos(pos)
        model.setScale(scale)
        model.setHpr(hpr)
        model.setColor(color)
        return model

    @staticmethod
    def create_stylized_counter(loader, parent, pos=(0,0,0), color=(0.4, 0.3, 0.2, 1)):
        root = parent.attachNewNode("counter")
        root.setPos(pos)

        # Base
        base = GeometryFactory.create_box(loader, root, pos=(0,0,0.4), scale=(1.2, 1.2, 0.8), color=color)

        # Top (Marble/Stone look)
        top = GeometryFactory.create_box(loader, root, pos=(0,0,0.85), scale=(1.3, 1.3, 0.1), color=(0.9, 0.9, 0.9, 1))

        # Bottom trim
        trim = GeometryFactory.create_box(loader, root, pos=(0,0,0.05), scale=(1.25, 1.25, 0.1), color=(color[0]*0.7, color[1]*0.7, color[2]*0.7, 1))

        return root

    @staticmethod
    def create_chef_hat(loader, parent, pos=(0,0,0)):
        root = parent.attachNewNode("chef_hat")
        root.setPos(pos)
        # Lower band
        GeometryFactory.create_box(loader, root, pos=(0,0,0.05), scale=(0.25, 0.25, 0.1), color=(1,1,1,1))
        # Floppy top
        GeometryFactory.create_sphere(loader, root, pos=(0,0,0.25), scale=(0.3, 0.3, 0.2), color=(1,1,1,1))
        return root

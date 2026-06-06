
from panda3d.core import Vec3, NodePath
from game.entities.item import Item
from game.utils.constants import Constants
from game.ui.progress_bar import ProgressBar
from game.utils.geometry_factory import GeometryFactory

class BaseStation:
    def __init__(self, base, pos, station_type, color=(0.4, 0.3, 0.2, 1)):
        self.base = base
        self.station_type = station_type

        self.model = GeometryFactory.create_stylized_counter(self.base.loader, self.base.render, pos, color)
        # For compatibility with existing code that looks for self.top
        self.top = self.model.find("**/box") # This is a bit brittle, but works if we know the structure

        self.content = None

    def interact(self, player):
        if player.held_item and not self.content:
            self.content = player.held_item
            self.content.model.reparentTo(self.model)
            self.content.model.setPos(0, 0, 1.0)
            player.held_item = None
            return True
        elif not player.held_item and self.content:
            player.pick_up(self.content)
            self.content = None
            return True
        return False

    def update(self, dt):
        pass

class IngredientCrate(BaseStation):
    def __init__(self, base, pos, ingredient_name):
        super().__init__(base, pos, Constants.STATION_CRATE, color=(0.2, 0.5, 0.2, 1))
        self.ingredient_name = ingredient_name

        # Add visual representation of ingredient on the crate
        Item(base, ingredient_name).model.reparentTo(self.model).setPos(0, 0, 1.0)

    def interact(self, player):
        if not player.held_item:
            item = Item(self.base, self.ingredient_name)
            player.pick_up(item)
            return True
        return False

class CuttingBoard(BaseStation):
    def __init__(self, base, pos):
        super().__init__(base, pos, Constants.STATION_CUTTING, color=(0.6, 0.4, 0.2, 1))

        # Cutting board visual
        self.board = GeometryFactory.create_box(self.base.loader, self.model, pos=(0, 0, 0.95), scale=(0.8, 0.8, 0.05), color=(0.9, 0.8, 0.6, 1))

        self.progress = 0
        self.is_cutting = False
        self.progress_bar = ProgressBar(self.model)

    def interact(self, player):
        if player.held_item and not self.content:
            if player.held_item.state == Constants.ITEM_RAW and player.held_item.name != "Plate":
                # Explicitly call super interaction or handle it here
                self.content = player.held_item
                self.content.model.reparentTo(self.model)
                self.content.model.setPos(0, 0, 1.05)
                player.held_item = None

                self.progress = 0
                self.is_cutting = True
                return True
        elif not player.held_item and self.content:
            if self.content.state == Constants.ITEM_CUT:
                player.pick_up(self.content)
                self.content = None
                self.is_cutting = False
                self.progress_bar.set_progress(0)
                return True
        return False

    def update(self, dt):
        if self.is_cutting and self.content:
            if self.base.sound_cut and self.base.sound_cut.status() != 2:
                self.base.sound_cut.play()
            self.progress += dt * 0.5
            self.progress_bar.set_progress(min(self.progress, 1.0))
            if self.progress >= 1.0:
                if self.base.sound_cut: self.base.sound_cut.stop()
                self.content.state = Constants.ITEM_CUT
                self.content.update_visual()
                self.is_cutting = False
                self.progress_bar.set_progress(0)

class Stove(BaseStation):
    def __init__(self, base, pos):
        super().__init__(base, pos, Constants.STATION_STOVE, color=(0.2, 0.2, 0.2, 1))

        # Burner visuals
        GeometryFactory.create_box(self.base.loader, self.model, pos=(0,0,0.91), scale=(0.7, 0.7, 0.02), color=(0.1, 0.1, 0.1, 1))
        self.burner = GeometryFactory.create_sphere(self.base.loader, self.model, pos=(0, 0, 0.92), scale=(0.3, 0.3, 0.02), color=(0.05, 0.05, 0.05, 1))

        self.progress = 0
        self.burn_progress = 0
        self.on_fire = False
        self.progress_bar = ProgressBar(self.model)

        self.fire_model = None

    def interact(self, player):
        if self.on_fire:
            if player.held_item and player.held_item.name == "extinguisher":
                self.on_fire = False
                self.burn_progress = 0
                if self.fire_model: self.fire_model.removeNode(); self.fire_model = None
                return True
            return False

        if player.held_item and not self.content:
            if player.held_item.state == Constants.ITEM_CUT:
                self.content = player.held_item
                self.content.model.reparentTo(self.model)
                self.content.model.setPos(0, 0, 1.1)
                player.held_item = None
                self.progress = 0
                self.burn_progress = 0
                return True
        elif not player.held_item and self.content:
            player.pick_up(self.content)
            self.content = None
            return True
        return False

    def update(self, dt):
        if self.content and not self.on_fire:
            if self.content.state == Constants.ITEM_CUT:
                if self.base.sound_cook and self.base.sound_cook.status() != 2:
                    self.base.sound_cook.play()
                self.progress += dt * 0.2
                self.progress_bar.set_color(0, 1, 0)
                self.progress_bar.set_progress(min(self.progress, 1.0))
                # Orange glow on burner
                self.burner.setColor(min(self.progress*2, 1.0), 0.2, 0, 1)
                if self.progress >= 1.0:
                    if self.base.sound_cook: self.base.sound_cook.stop()
                    self.content.state = Constants.ITEM_COOKED
                    self.content.update_visual()
            elif self.content.state == Constants.ITEM_COOKED:
                if self.base.sound_cook and self.base.sound_cook.status() != 2:
                    self.base.sound_cook.play()
                self.burn_progress += dt * 0.1
                self.progress_bar.set_color(1, 0, 0)
                self.progress_bar.set_progress(min(self.burn_progress, 1.0))
                self.burner.setColor(1, 0, 0, 1)
                if self.burn_progress >= 1.0:
                    if self.base.sound_cook: self.base.sound_cook.stop()
                    self.content.state = Constants.ITEM_BURNT
                    self.content.update_visual()
                    self.on_fire = True
                    self.progress_bar.set_progress(0)
                    self.fire_model = GeometryFactory.create_sphere(self.base.loader, self.model, pos=(0,0,1.5), scale=0.8, color=(1, 0.5, 0, 0.7))
                    if self.base.sound_fire: self.base.sound_fire.play()
            else:
                if self.base.sound_cook: self.base.sound_cook.stop()
                self.progress_bar.set_progress(0)
                self.burner.setColor(0.05, 0.05, 0.05, 1)
        else:
            if not self.on_fire and self.base.sound_cook: self.base.sound_cook.stop()
            self.progress_bar.set_progress(0)
            if not self.on_fire: self.burner.setColor(0.05, 0.05, 0.05, 1)

class TrashBin(BaseStation):
    def __init__(self, base, pos):
        # Trash bin is taller and thinner
        super().__init__(base, pos, Constants.STATION_TRASH, color=(0.15, 0.15, 0.15, 1))
        self.model.setScale(0.8, 0.8, 1.2)
        # Lid visual
        GeometryFactory.create_box(self.base.loader, self.model, pos=(0,0,0.9), scale=(1.1, 1.1, 0.1), color=(0.2, 0.2, 0.2, 1))

    def interact(self, player):
        if player.held_item:
            player.held_item.destroy()
            player.held_item = None
            return True
        return False

class Counter(BaseStation):
    def __init__(self, base, pos, order_manager):
        super().__init__(base, pos, Constants.STATION_COUNTER, color=(0.3, 0.5, 0.7, 1))
        self.order_manager = order_manager

    def interact(self, player):
        if player.held_item:
            if player.held_item.name == "Plate":
                self.content = player.held_item
                self.content.model.reparentTo(self.model)
                self.content.model.setPos(0, 0, 1.0)
                player.held_item = None
                return True
            else:
                if self.content and self.content.name == "Plate":
                    plate = self.content
                    plate.contents.append(player.held_item)
                    player.held_item.model.reparentTo(plate.model)
                    player.held_item.model.setPos(0, 0, 0.2 + len(plate.contents)*0.2)
                    player.held_item = None
                    return True
                else:
                    self.content = player.held_item
                    self.content.model.reparentTo(self.model)
                    self.content.model.setPos(0, 0, 1.0)
                    player.held_item = None
                    return True
        elif not player.held_item and self.content:
            if self.content.name == "Plate":
                plate = self.content
                if self.order_manager.complete_order(plate.contents):
                    for item in plate.contents:
                        item.destroy()
                    plate.contents = []
                    return True
                else:
                    player.pick_up(self.content)
                    self.content = None
                    return True
            else:
                player.pick_up(self.content)
                self.content = None
                return True
        return False

class PlateCrate(BaseStation):
    def __init__(self, base, pos):
        super().__init__(base, pos, Constants.STATION_CRATE, color=(0.8, 0.8, 0.8, 1))
        # Visual plates
        for i in range(3):
            GeometryFactory.create_box(self.base.loader, self.model, pos=(0, 0, 0.9 + i*0.1), scale=(0.8, 0.8, 0.05), color=(0.9, 0.9, 0.9, 1))

    def interact(self, player):
        if not player.held_item:
            item = Item(self.base, "Plate")
            player.pick_up(item)
            return True
        return False

class DiningTable(BaseStation):
    def __init__(self, base, pos):
        # We don't use the BaseStation counter model here
        self.base = base
        self.station_type = "dining_table"
        self.model = self.base.render.attachNewNode("dining_table")
        self.model.setPos(pos)

        # Table top
        self.table_top = GeometryFactory.create_box(self.base.loader, self.model, pos=(0,0,0.8), scale=(2.5, 1.5, 0.1), color=(0.5, 0.3, 0.2, 1))
        # Legs
        for lx, ly in [(-1, -0.6), (1, -0.6), (-1, 0.6), (1, 0.6)]:
            GeometryFactory.create_box(self.base.loader, self.model, pos=(lx, ly, 0.4), scale=(0.1, 0.1, 0.8), color=(0.3, 0.2, 0.1, 1))

        self.occupied_by = None
        self.content = None

    def interact(self, player):
        # Player can drop food on table for customers
        if player.held_item and not self.content:
            self.content = player.held_item
            self.content.model.reparentTo(self.model)
            self.content.model.setPos(0, 0, 0.9)
            player.held_item = None
            return True
        elif not player.held_item and self.content:
            player.pick_up(self.content)
            self.content = None
            return True
        return False

class ExtinguisherStation(BaseStation):
    def __init__(self, base, pos):
        super().__init__(base, pos, Constants.STATION_EXTINGUISHER, color=(0.8, 0.2, 0.2, 1))
        # Visual extinguisher
        Item(base, "extinguisher").model.reparentTo(self.model).setPos(0, 0, 1.2)

    def interact(self, player):
        if not player.held_item:
            item = Item(self.base, "extinguisher")
            player.pick_up(item)
            return True
        elif player.held_item and player.held_item.name == "extinguisher":
            player.held_item.destroy()
            player.held_item = None
            return True
        return False

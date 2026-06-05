
from panda3d.core import Vec3
from game.entities.item import Item
from game.utils.constants import Constants
from game.ui.progress_bar import ProgressBar

class BaseStation:
    def __init__(self, base, pos, station_type):
        self.base = base
        self.station_type = station_type

        # Visual
        self.model = self.base.loader.loadModel("models/box")
        self.model.reparentTo(self.base.render)
        self.model.setPos(pos)
        self.model.setScale(1.0, 1.0, 0.8)
        self.model.setColor(0.5, 0.5, 0.5, 1)

        self.content = None

    def interact(self, player):
        # Base interaction: Swap item between player and station
        if player.held_item and not self.content:
            # Player gives to station
            self.content = player.held_item
            self.content.model.reparentTo(self.model)
            self.content.model.setPos(0, 0, 1.0)
            player.held_item = None
            return True
        elif not player.held_item and self.content:
            # Player takes from station
            player.pick_up(self.content)
            self.content = None
            return True
        return False

    def update(self, dt):
        pass

class IngredientCrate(BaseStation):
    def __init__(self, base, pos, ingredient_name):
        super().__init__(base, pos, Constants.STATION_CRATE)
        self.ingredient_name = ingredient_name
        self.model.setColor(0.2, 0.5, 0.2, 1)

    def interact(self, player):
        if not player.held_item:
            item = Item(self.base, self.ingredient_name)
            player.pick_up(item)
            return True
        return False

class CuttingBoard(BaseStation):
    def __init__(self, base, pos):
        super().__init__(base, pos, Constants.STATION_CUTTING)
        self.model.setColor(0.8, 0.8, 0.5, 1)
        self.progress = 0
        self.is_cutting = False
        self.progress_bar = ProgressBar(self.model)

    def interact(self, player):
        if player.held_item and not self.content:
            if player.held_item.state == Constants.ITEM_RAW and player.held_item.name != "Plate":
                super().interact(player)
                self.progress = 0
                self.is_cutting = True
                return True
        elif not player.held_item and self.content:
            if self.content.state == Constants.ITEM_CUT:
                super().interact(player)
                self.is_cutting = False
                return True
        return False

    def update(self, dt):
        if self.is_cutting and self.content:
            self.progress += dt * 0.5 # 2 seconds to cut
            self.progress_bar.set_progress(min(self.progress, 1.0))
            if self.progress >= 1.0:
                self.content.state = Constants.ITEM_CUT
                self.content.update_visual()
                self.is_cutting = False
                self.progress_bar.set_progress(0)

class Stove(BaseStation):
    def __init__(self, base, pos):
        super().__init__(base, pos, Constants.STATION_STOVE)
        self.model.setColor(1, 0.2, 0.2, 1)
        self.progress = 0
        self.burn_progress = 0
        self.on_fire = False
        self.progress_bar = ProgressBar(self.model)

    def interact(self, player):
        if self.on_fire:
            if player.held_item and player.held_item.name == "extinguisher":
                self.on_fire = False
                self.burn_progress = 0
                return True
            return False

        if player.held_item and not self.content:
            if player.held_item.state == Constants.ITEM_CUT:
                super().interact(player)
                self.progress = 0
                self.burn_progress = 0
                return True
        elif not player.held_item and self.content:
            super().interact(player)
            return True
        return False

    def update(self, dt):
        if self.content and not self.on_fire:
            if self.content.state == Constants.ITEM_CUT:
                self.progress += dt * 0.2 # 5 seconds to cook
                self.progress_bar.set_color(0, 1, 0)
                self.progress_bar.set_progress(min(self.progress, 1.0))
                if self.progress >= 1.0:
                    self.content.state = Constants.ITEM_COOKED
                    self.content.update_visual()
            elif self.content.state == Constants.ITEM_COOKED:
                self.burn_progress += dt * 0.1 # 10 seconds to burn
                self.progress_bar.set_color(1, 0, 0)
                self.progress_bar.set_progress(min(self.burn_progress, 1.0))
                if self.burn_progress >= 1.0:
                    self.content.state = Constants.ITEM_BURNT
                    self.content.update_visual()
                    self.on_fire = True
                    self.progress_bar.set_progress(0)
                    if self.base.sound_fire: self.base.sound_fire.play()
                    print("FIRE!")
            else:
                self.progress_bar.set_progress(0)
        else:
            self.progress_bar.set_progress(0)

class TrashBin(BaseStation):
    def __init__(self, base, pos):
        super().__init__(base, pos, Constants.STATION_TRASH)
        self.model.setColor(0.1, 0.1, 0.1, 1)

    def interact(self, player):
        if player.held_item:
            player.held_item.destroy()
            player.held_item = None
            return True
        return False

class Counter(BaseStation):
    def __init__(self, base, pos, order_manager):
        super().__init__(base, pos, Constants.STATION_COUNTER)
        self.order_manager = order_manager
        self.model.setColor(0.7, 0.7, 0.7, 1)
        self.plate_contents = []

    def interact(self, player):
        if player.held_item:
            if player.held_item.name == "Plate":
                # Swap plate or something?
                super().interact(player)
            else:
                # If there's a plate on the counter, add item to it
                if self.content and self.content.name == "Plate":
                    self.plate_contents.append(player.held_item)
                    player.held_item.model.reparentTo(self.content.model)
                    player.held_item.model.setPos(0, 0, 0.2 + len(self.plate_contents)*0.2)
                    player.held_item = None
                else:
                    super().interact(player)
        elif not player.held_item and self.content:
            if self.content.name == "Plate":
                # Try to serve
                if self.order_manager.complete_order(self.plate_contents):
                    # Success, clear plate
                    for item in self.plate_contents:
                        item.destroy()
                    self.plate_contents = []
                    # Keep the plate or serve the plate? Let's say we serve the plate and it reappears.
                    return True
                else:
                    # Just pick up the plate
                    super().interact(player)
            else:
                super().interact(player)
        return False

class PlateCrate(BaseStation):
    def __init__(self, base, pos):
        super().__init__(base, pos, Constants.STATION_CRATE)
        self.model.setColor(1, 1, 1, 1)

    def interact(self, player):
        if not player.held_item:
            item = Item(self.base, "Plate")
            item.model.setColor(0.9, 0.9, 0.9, 1)
            player.pick_up(item)
            return True
        return False

class ExtinguisherStation(BaseStation):
    def __init__(self, base, pos):
        super().__init__(base, pos, Constants.STATION_EXTINGUISHER)
        self.model.setColor(1, 0, 0, 1)

    def interact(self, player):
        if not player.held_item:
            item = Item(self.base, "extinguisher")
            item.model.setColor(1, 0, 0, 1)
            player.pick_up(item)
            return True
        elif player.held_item and player.held_item.name == "extinguisher":
            player.held_item.destroy()
            player.held_item = None
            return True
        return False


from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectButton, DirectFrame, OnscreenText
from panda3d.core import TextNode
import sys
import json
import os

from game.utils.constants import Constants
from game.utils.input_manager import InputManager
from game.entities.player import Player
from game.entities.stations import (
    BaseStation, IngredientCrate, CuttingBoard, Stove, TrashBin, ExtinguisherStation,
    Counter, PlateCrate
)
from game.utils.order_manager import OrderManager

class CookingGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse() # We want direct control over the camera

        self.state = Constants.STATE_MENU
        self.key_map = self.load_keybindings()
        self.input_manager = InputManager(self, self.key_map)

        # UI Containers
        self.menu_frame = None
        self.options_frame = None
        self.game_ui_frame = None
        self.gameover_frame = None

        self.setup_ui()
        self.enter_state(Constants.STATE_MENU)

    def load_keybindings(self):
        if os.path.exists("keybindings.json"):
            with open("keybindings.json", "r") as f:
                return json.load(f)
        return Constants.DEFAULT_KEYS.copy()

    def save_keybindings(self):
        with open("keybindings.json", "w") as f:
            json.dump(self.key_map, f)

    def setup_ui(self):
        # Main Menu
        self.menu_frame = DirectFrame(frameColor=(0, 0, 0, 0.5), frameSize=(-0.5, 0.5, -0.5, 0.5))
        self.menu_title = OnscreenText(text="Cooking Adventure Clone", pos=(0, 0.3), scale=0.1, parent=self.menu_frame, fg=(1,1,1,1))

        self.btn_play = DirectButton(text="Lancer une partie", scale=0.08, pos=(0, 0.1, 0),
                                     parent=self.menu_frame, command=self.start_game)
        self.btn_options = DirectButton(text="Options", scale=0.08, pos=(0, -0.1, 0),
                                        parent=self.menu_frame, command=lambda: self.enter_state(Constants.STATE_OPTIONS))
        self.btn_quit = DirectButton(text="Quitter", scale=0.08, pos=(0, -0.3, 0),
                                     parent=self.menu_frame, command=sys.exit)

        # Sounds
        try:
            self.sound_interact = self.loader.loadSfx("assets/sounds/interact.wav")
            self.sound_success = self.loader.loadSfx("assets/sounds/success.wav")
            self.sound_fail = self.loader.loadSfx("assets/sounds/fail.wav")
            self.sound_fire = self.loader.loadSfx("assets/sounds/fire.wav")
            self.sound_fire.setLoop(True)
        except:
            print("Warning: Could not load sounds.")
            self.sound_interact = None
            self.sound_success = None
            self.sound_fail = None
            self.sound_fire = None

        self.menu_frame.hide()

        # Options Menu
        self.options_frame = DirectFrame(frameColor=(0, 0, 0, 0.7), frameSize=(-0.8, 0.8, -0.8, 0.8))
        OnscreenText(text="Options - Configuration des touches", pos=(0, 0.6), scale=0.1, parent=self.options_frame, fg=(1,1,1,1))

        self.key_buttons = {}
        y_pos = 0.4
        for action in self.key_map:
            text = f"{action}: {self.key_map[action]}"
            btn = DirectButton(text=text, scale=0.06, pos=(0, y_pos, 0),
                               parent=self.options_frame, command=self.start_rebind, extraArgs=[action])
            self.key_buttons[action] = btn
            y_pos -= 0.12

        DirectButton(text="Retour", scale=0.08, pos=(0, -0.6, 0),
                     parent=self.options_frame, command=lambda: self.enter_state(Constants.STATE_MENU))
        self.options_frame.hide()
        self.rebinding_action = None

        # Game UI
        self.game_ui_frame = DirectFrame(frameColor=(0, 0, 0, 0), frameSize=(-1, 1, -1, 1))
        self.score_text = OnscreenText(text="Score: 0", pos=(-1.1, 0.9), scale=0.07, parent=self.game_ui_frame, fg=(1,1,1,1), align=TextNode.ALeft)
        self.timer_text = OnscreenText(text="Temps: 180", pos=(1.1, 0.9), scale=0.07, parent=self.game_ui_frame, fg=(1,1,1,1), align=TextNode.ARight)
        self.orders_text = OnscreenText(text="", pos=(-1.1, 0.7), scale=0.05, parent=self.game_ui_frame, fg=(1,1,1,1), align=TextNode.ALeft, mayChange=True)
        self.game_ui_frame.hide()

        # Game Over UI
        self.gameover_frame = DirectFrame(frameColor=(0, 0, 0, 0.8), frameSize=(-0.7, 0.7, -0.7, 0.7))
        self.gameover_title = OnscreenText(text="FIN DE PARTIE", pos=(0, 0.4), scale=0.12, parent=self.gameover_frame, fg=(1,0,0,1))
        self.final_score_text = OnscreenText(text="Score Final: 0", pos=(0, 0.1), scale=0.08, parent=self.gameover_frame, fg=(1,1,1,1))
        DirectButton(text="Menu Principal", scale=0.08, pos=(0, -0.3, 0),
                     parent=self.gameover_frame, command=lambda: self.enter_state(Constants.STATE_MENU))
        self.gameover_frame.hide()

    def start_rebind(self, action):
        self.rebinding_action = action
        self.key_buttons[action].setText(f"Appuyez sur une touche pour {action}...")
        # In Panda3D, to catch any key, we can use 'time-any' or just a task that monitors button presses
        self.button_thrower_node = self.buttonThrowers[0].node()
        self.accept("button-down", self.finish_rebind)

    def finish_rebind(self, key):
        if self.rebinding_action:
            # We don't want to bind 'escape' or 'mouse1' by accident usually, but let's be flexible
            self.key_map[self.rebinding_action] = key
            self.key_buttons[self.rebinding_action].setText(f"{self.rebinding_action}: {key}")
            self.save_keybindings()
            self.input_manager.update_keymap(self.key_map)
            self.rebinding_action = None
            self.ignore("button-down")

    def cleanup_game(self):
        if hasattr(self, 'player') and self.player:
            self.player.model.removeNode()
            if self.player.held_item:
                self.player.held_item.destroy()
            self.player = None

        if hasattr(self, 'stations'):
            for station in self.stations:
                if station.content:
                    station.content.destroy()
                if hasattr(station, 'plate_contents'):
                    for item in station.plate_contents:
                        item.destroy()
                station.model.removeNode()
            self.stations = []

        if hasattr(self, 'order_manager'):
            self.order_manager = None

        if self.sound_fire:
            self.sound_fire.stop()

        self.taskMgr.remove("update_task")

    def enter_state(self, new_state):
        if self.state == Constants.STATE_PLAYING and new_state != Constants.STATE_PLAYING:
            pass # Keep it for gameover display? No, better cleanup and show results.

        self.menu_frame.hide()
        self.options_frame.hide()
        self.game_ui_frame.hide()
        self.gameover_frame.hide()

        self.state = new_state

        if self.state == Constants.STATE_MENU:
            self.menu_frame.show()
        elif self.state == Constants.STATE_OPTIONS:
            self.options_frame.show()
        elif self.state == Constants.STATE_PLAYING:
            self.cleanup_game() # Clear any previous game
            self.game_ui_frame.show()
            self.setup_game_world()
        elif self.state == Constants.STATE_GAMEOVER:
            self.final_score_text.setText(f"Score Final: {self.score}")
            self.gameover_frame.show()

    def start_game(self):
        self.enter_state(Constants.STATE_PLAYING)

    def setup_game_world(self):
        print("Starting game world...")
        self.player = Player(self, self.input_manager)
        self.order_manager = OrderManager(self)
        self.score = 0
        self.level_time = 180.0 # 3 minutes

        # Layout
        self.stations = []
        # Crates
        self.stations.append(IngredientCrate(self, (-4, 4, 0), "Tomato"))
        self.stations.append(IngredientCrate(self, (-2, 4, 0), "Onion"))

        # Cutting Boards
        self.stations.append(CuttingBoard(self, (0, 4, 0)))

        # Stoves
        self.stations.append(Stove(self, (2, 4, 0)))
        self.stations.append(Stove(self, (4, 4, 0)))

        # Utilities
        self.stations.append(TrashBin(self, (6, 4, 0)))
        self.stations.append(ExtinguisherStation(self, (-6, 4, 0)))

        # Counter and Plates
        self.stations.append(Counter(self, (0, -4, 0), self.order_manager))
        self.stations.append(PlateCrate(self, (-2, -4, 0)))

        self.camera.setPos(0, -12, 12)
        self.camera.lookAt(0, 0, 0)

        self.taskMgr.add(self.update, "update_task")

    def update(self, task):
        dt = globalClock.getDt()

        if self.state == Constants.STATE_PLAYING:
            any_fire = False
            self.level_time -= dt
            if self.level_time <= 0:
                self.enter_state(Constants.STATE_GAMEOVER)
                return task.cont

            self.player.update(dt)
            self.order_manager.update(dt)

            for station in self.stations:
                station.update(dt)
                if hasattr(station, 'on_fire') and station.on_fire:
                    any_fire = True

            if any_fire:
                if self.sound_fire and self.sound_fire.status() != self.sound_fire.PLAYING:
                    self.sound_fire.play()
            else:
                if self.sound_fire: self.sound_fire.stop()

            self.update_ui()

            if self.input_manager.is_pressed("interact"):
                self.handle_interaction()
                # Reset interact key to prevent spam
                self.input_manager.pressed_keys["interact"] = False

        return task.cont

    def update_ui(self):
        self.score_text.setText(f"Score: {self.score}")
        self.timer_text.setText(f"Temps: {int(self.level_time)}")

        orders_str = "Commandes:\n"
        for order in self.order_manager.active_orders:
            orders_str += f"- {order.recipe_name} ({int(order.time_left)}s)\n"
        self.orders_text.setText(orders_str)

    def handle_interaction(self):
        # Simple distance-based interaction
        for station in self.stations:
            dist = (self.player.model.getPos() - station.model.getPos()).length()
            if dist < 1.5:
                if station.interact(self.player):
                    if self.sound_interact: self.sound_interact.play()
                break

if __name__ == "__main__":
    app = CookingGame()
    app.run()

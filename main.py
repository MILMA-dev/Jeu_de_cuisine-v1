

from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectButton, DirectFrame, OnscreenText
from panda3d.core import TextNode, WindowProperties, loadPrcFileData, AmbientLight, DirectionalLight, Vec4
import simplepbr
import sys
import json
import os

from game.utils.constants import Constants
from game.utils.input_manager import InputManager
from game.entities.player import Player
from game.entities.stations import (
    BaseStation, IngredientCrate, CuttingBoard, Stove, TrashBin, ExtinguisherStation,
    Counter, PlateCrate, DiningTable
)
from game.entities.environment import Environment
from game.utils.order_manager import OrderManager

class CookingGame(ShowBase):
    def __init__(self):
        loadPrcFileData("", "window-title Cooking Adventure Clone")
        loadPrcFileData("", "win-size 1280 720")
        loadPrcFileData("", "textures-power-2 none")

        ShowBase.__init__(self)
        self.disableMouse()

        self.pipeline = simplepbr.init()

        self.state = Constants.STATE_MENU
        self.key_map = self.load_keybindings()
        self.input_manager = InputManager(self, self.key_map)

        self.setup_ui()
        self.enter_state(Constants.STATE_MENU)

    def load_keybindings(self):
        if os.path.exists("keybindings.json"):
            try:
                with open("keybindings.json", "r") as f:
                    return json.load(f)
            except:
                return Constants.DEFAULT_KEYS.copy()
        return Constants.DEFAULT_KEYS.copy()

    def save_keybindings(self):
        with open("keybindings.json", "w") as f:
            json.dump(self.key_map, f)

    def setup_ui(self):
        # Background color for menus
        self.setBackgroundColor(0.2, 0.4, 0.6)

        # Main Menu
        self.menu_frame = DirectFrame(frameColor=(0, 0, 0, 0.6), frameSize=(-0.6, 0.6, -0.7, 0.7))
        OnscreenText(text="COOKING ADVENTURE", pos=(0, 0.5), scale=0.15, parent=self.menu_frame, fg=(1, 0.8, 0.2, 1), font=self.loader.loadFont("models/cmss12"))

        btn_style = {"scale": 0.08, "frameColor": (0.8, 0.4, 0.2, 1), "text_fg": (1,1,1,1), "relief": 1}

        self.btn_play = DirectButton(text="COMMENCER", pos=(0, 0.2, 0), parent=self.menu_frame, command=self.start_game, **btn_style)
        self.btn_options = DirectButton(text="OPTIONS", pos=(0, 0.0, 0), parent=self.menu_frame, command=lambda: self.enter_state(Constants.STATE_OPTIONS), **btn_style)
        self.btn_quit = DirectButton(text="QUITTER", pos=(0, -0.2, 0), parent=self.menu_frame, command=sys.exit, **btn_style)

        # Options Menu
        self.options_frame = DirectFrame(frameColor=(0, 0, 0, 0.8), frameSize=(-0.9, 0.9, -0.9, 0.9))
        OnscreenText(text="CONFIGURATION DES TOUCHES", pos=(0, 0.7), scale=0.1, parent=self.options_frame, fg=(1,1,1,1))

        self.key_buttons = {}
        actions = ["up", "down", "left", "right", "interact"]
        labels = {"up": "Avancer (Z)", "down": "Reculer (S)", "left": "Gauche (Q)", "right": "Droite (D)", "interact": "Action (E)"}

        y_pos = 0.4
        for action in actions:
            text = f"{labels[action]}: {self.key_map[action]}"
            btn = DirectButton(text=text, scale=0.06, pos=(0, y_pos, 0),
                               parent=self.options_frame, command=self.start_rebind, extraArgs=[action], frameSize=(-6, 6, -0.6, 1.2))
            self.key_buttons[action] = btn
            y_pos -= 0.18

        DirectButton(text="RETOUR", scale=0.07, pos=(0, -0.6, 0),
                     parent=self.options_frame, command=lambda: self.enter_state(Constants.STATE_MENU), **btn_style)
        self.options_frame.hide()

        # Game UI
        self.game_ui_frame = DirectFrame(frameColor=(0, 0, 0, 0), frameSize=(-1, 1, -1, 1))
        self.score_text = OnscreenText(text="Score: 0", pos=(-1.2, 0.9), scale=0.08, parent=self.game_ui_frame, fg=(1,1,1,1), align=TextNode.ALeft)
        self.timer_text = OnscreenText(text="Temps: 180", pos=(1.2, 0.9), scale=0.08, parent=self.game_ui_frame, fg=(1,1,1,1), align=TextNode.ARight)
        self.game_ui_frame.hide()

        # Game Over UI
        self.gameover_frame = DirectFrame(frameColor=(0, 0, 0, 0.9), frameSize=(-0.7, 0.7, -0.7, 0.7))
        OnscreenText(text="PARTIE TERMINÉE", pos=(0, 0.4), scale=0.12, parent=self.gameover_frame, fg=(1, 0.2, 0.2, 1))
        self.final_score_text = OnscreenText(text="Score Final: 0", pos=(0, 0.1), scale=0.08, parent=self.gameover_frame, fg=(1,1,1,1))
        DirectButton(text="MENU PRINCIPAL", pos=(0, -0.3, 0), parent=self.gameover_frame, command=lambda: self.enter_state(Constants.STATE_MENU), **btn_style)
        self.gameover_frame.hide()

        try:
            self.sound_interact = self.loader.loadSfx("assets/sounds/interact.wav")
            self.sound_success = self.loader.loadSfx("assets/sounds/success.wav")
            self.sound_fail = self.loader.loadSfx("assets/sounds/fail.wav")
            self.sound_fire = self.loader.loadSfx("assets/sounds/fire.wav")
            self.sound_fire.setLoop(True)
        except:
            self.sound_interact = self.sound_success = self.sound_fail = self.sound_fire = None

    def start_rebind(self, action):
        self.rebinding_action = action
        self.key_buttons[action].setText("Appuyez sur une touche...")
        self.accept("button-down", self.finish_rebind)

    def finish_rebind(self, key):
        if hasattr(self, 'rebinding_action') and self.rebinding_action:
            self.key_map[self.rebinding_action] = key
            self.key_buttons[self.rebinding_action].setText(f"{self.rebinding_action.upper()}: {key}")
            self.save_keybindings()
            self.input_manager.update_keymap(self.key_map)
            self.rebinding_action = None
            self.ignore("button-down")

    def enter_state(self, new_state):
        self.menu_frame.hide()
        self.options_frame.hide()
        self.game_ui_frame.hide()
        self.gameover_frame.hide()

        self.state = new_state

        if self.state == Constants.STATE_MENU:
            self.menu_frame.show()
            self.setBackgroundColor(0.2, 0.4, 0.6)
        elif self.state == Constants.STATE_OPTIONS:
            self.options_frame.show()
        elif self.state == Constants.STATE_PLAYING:
            self.cleanup_game()
            self.game_ui_frame.show()
            self.setup_game_world()
        elif self.state == Constants.STATE_GAMEOVER:
            self.final_score_text.setText(f"Score Final: {self.score}")
            self.gameover_frame.show()

    def cleanup_game(self):
        if hasattr(self, 'player') and self.player:
            self.player.model.removeNode()
            if self.player.held_item: self.player.held_item.destroy()
            self.player = None

        if hasattr(self, 'customers'):
            for c in self.customers: c.model.removeNode()
            self.customers = []

        if hasattr(self, 'stations'):
            for s in self.stations:
                if s.content: s.content.destroy()
                s.model.removeNode()
            self.stations = []

        if hasattr(self, 'environment') and self.environment:
            self.environment.root.removeNode()

        self.taskMgr.remove("update_task")
        if self.sound_fire: self.sound_fire.stop()

    def start_game(self):
        self.enter_state(Constants.STATE_PLAYING)

    def setup_game_world(self):
        self.setBackgroundColor(0.5, 0.7, 0.9)

        alight = AmbientLight('alight')
        alight.setColor(Vec4(0.6, 0.6, 0.6, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)

        dlight = DirectionalLight('dlight')
        dlight.setColor(Vec4(1.0, 1.0, 0.9, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(45, -60, 0)
        self.render.setLight(dlnp)

        self.environment = Environment(self)
        self.player = Player(self, self.input_manager)
        self.order_manager = OrderManager(self)
        self.customers = []
        self.score = 0
        self.level_time = 180.0

        self.stations = []
        # Layout
        self.stations.append(ExtinguisherStation(self, (-8, 8, 0)))
        self.stations.append(IngredientCrate(self, (-6, 8, 0), "Tomato"))
        self.stations.append(IngredientCrate(self, (-4, 8, 0), "Onion"))
        self.stations.append(IngredientCrate(self, (-2, 8, 0), "Meat"))
        self.stations.append(CuttingBoard(self, (0, 8, 0)))
        self.stations.append(Stove(self, (2, 8, 0)))
        self.stations.append(Stove(self, (4, 8, 0)))
        self.stations.append(TrashBin(self, (6, 8, 0)))

        self.stations.append(PlateCrate(self, (-3, 2, 0)))
        self.stations.append(Counter(self, (0, 2, 0), self.order_manager))
        self.stations.append(Counter(self, (3, 2, 0), self.order_manager))

        self.stations.append(DiningTable(self, (-5, -5, 0)))
        self.stations.append(DiningTable(self, (0, -5, 0)))
        self.stations.append(DiningTable(self, (5, -5, 0)))

        self.camera.setPos(0, -22, 22)
        self.camera.lookAt(0, -2, 0)

        self.taskMgr.add(self.update, "update_task")

    def update(self, task):
        dt = globalClock.getDt()
        if self.state == Constants.STATE_PLAYING:
            self.level_time -= dt
            if self.level_time <= 0:
                self.enter_state(Constants.STATE_GAMEOVER)
                return task.cont

            self.player.update(dt)
            self.order_manager.update(dt)
            for c in self.customers[:]: c.update(dt)

            any_fire = False
            for s in self.stations:
                s.update(dt)
                if hasattr(s, 'on_fire') and s.on_fire: any_fire = True

            if any_fire and self.sound_fire and self.sound_fire.status() != 2: self.sound_fire.play()
            elif not any_fire and self.sound_fire: self.sound_fire.stop()

            self.update_ui()
            if self.input_manager.is_pressed("interact"):
                self.handle_interaction()
                self.input_manager.pressed_keys["interact"] = False

        return task.cont

    def update_ui(self):
        self.score_text.setText(f"Score: {self.score}")
        self.timer_text.setText(f"Temps: {int(self.level_time)}")

    def handle_interaction(self):
        for station in self.stations:
            dist = (self.player.model.getPos() - station.model.getPos()).length()
            if dist < 1.8:
                if station.interact(self.player):
                    if self.sound_interact: self.sound_interact.play()
                break

if __name__ == "__main__":
    app = CookingGame()
    app.run()

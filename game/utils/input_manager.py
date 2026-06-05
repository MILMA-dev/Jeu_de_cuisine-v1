
from panda3d.core import KeyboardButton

class InputManager:
    def __init__(self, base, key_map):
        self.base = base
        self.key_map = key_map
        self.pressed_keys = {action: False for action in key_map}
        self.setup_listeners()

    def setup_listeners(self):
        for action, key in self.key_map.items():
            self.base.accept(key, self.set_key, [action, True])
            self.base.accept(key + "-up", self.set_key, [action, False])

    def set_key(self, action, is_pressed):
        self.pressed_keys[action] = is_pressed

    def is_pressed(self, action):
        return self.pressed_keys.get(action, False)

    def update_keymap(self, new_key_map):
        # Ignore previous listeners
        for key in self.key_map.values():
            self.base.ignore(key)
            self.base.ignore(key + "-up")

        self.key_map = new_key_map
        self.pressed_keys = {action: False for action in self.key_map}
        self.setup_listeners()

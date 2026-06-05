
from game.utils.constants import Constants

class InputManager:
    def __init__(self, base, key_map):
        self.base = base
        self.key_map = key_map
        self.pressed_keys = {action: False for action in key_map}

        self.setup_bindings()

    def setup_bindings(self):
        # Clear existing bindings if any
        self.base.ignoreAll()
        for action, key in self.key_map.items():
            self.base.accept(key, self.set_key, [action, True])
            self.base.accept(f"{key}-up", self.set_key, [action, False])

        # Support for escape to pause or back
        self.base.accept("escape", self.handle_escape)

    def set_key(self, action, val):
        self.pressed_keys[action] = val

    def is_pressed(self, action):
        return self.pressed_keys.get(action, False)

    def update_keymap(self, new_key_map):
        self.key_map = new_key_map
        self.pressed_keys = {action: False for action in self.key_map}
        self.setup_bindings()

    def handle_escape(self):
        if self.base.state == Constants.STATE_PLAYING:
            self.base.enter_state(Constants.STATE_MENU)
        elif self.base.state == Constants.STATE_OPTIONS:
            self.base.enter_state(Constants.STATE_MENU)

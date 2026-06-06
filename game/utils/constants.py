
class Constants:
    # Game States
    STATE_MENU = "menu"
    STATE_OPTIONS = "options"
    STATE_PLAYING = "playing"
    STATE_PAUSED = "paused"
    STATE_GAMEOVER = "gameover"
    STATE_LEVEL_SELECT = "level_select"

    # Default Keybindings (AZERTY)
    DEFAULT_KEYS = {
        "up": "z",
        "down": "s",
        "left": "q",
        "right": "d",
        "interact": "e",
        "dash": "shift",
        "quit": "escape"
    }

    # Station Types
    STATION_CRATE = "crate"
    STATION_CUTTING = "cutting"
    STATION_STOVE = "stove"
    STATION_TRASH = "trash"
    STATION_COUNTER = "counter"
    STATION_EXTINGUISHER = "extinguisher"

    # Item States
    ITEM_RAW = "raw"
    ITEM_CUT = "cut"
    ITEM_COOKED = "cooked"
    ITEM_BURNT = "burnt"

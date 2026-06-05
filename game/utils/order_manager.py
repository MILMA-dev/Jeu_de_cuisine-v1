
import random
from game.utils.constants import Constants

class Order:
    def __init__(self, recipe_name, ingredients):
        self.recipe_name = recipe_name
        self.ingredients = ingredients # List of (name, state)
        self.time_left = 60.0 # 60 seconds to complete
        self.max_time = 60.0

class OrderManager:
    def __init__(self, base):
        self.base = base
        self.active_orders = []
        self.recipes = {
            # Entrées
            "Salade de Tomate": [("Tomato", Constants.ITEM_CUT)],
            "Rondelles d'Oignons": [("Onion", Constants.ITEM_CUT)],
            # Plats Principaux
            "Soupe d'Oignon": [("Onion", Constants.ITEM_COOKED)],
            "Ratatouille Express": [("Tomato", Constants.ITEM_COOKED), ("Onion", Constants.ITEM_COOKED)],
            # Desserts
            "Sorbet Tomate": [("Tomato", Constants.ITEM_RAW)], # Prototype simplicity
            # Boissons
            "Jus de Tomate": [("Tomato", Constants.ITEM_CUT)], # Represented by cut tomato for now
            "Infusion d'Oignon": [("Onion", Constants.ITEM_COOKED)]
        }
        self.spawn_timer = 0

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > 15.0: # New order every 15 seconds
            self.spawn_order()
            self.spawn_timer = 0

        for order in self.active_orders:
            order.time_left -= dt
            if order.time_left <= 0:
                self.fail_order(order)

    def spawn_order(self):
        if len(self.active_orders) < 5:
            name = random.choice(list(self.recipes.keys()))
            order = Order(name, self.recipes[name])
            self.active_orders.append(order)
            print(f"Nouvelle commande : {name}")

    def fail_order(self, order):
        print(f"Commande échouée : {order.recipe_name}")
        self.active_orders.remove(order)
        self.base.score = max(0, self.base.score - 50)
        if self.base.sound_fail: self.base.sound_fail.play()

    def complete_order(self, items):
        # items is a list of Item objects
        for order in self.active_orders:
            if self.match_recipe(order, items):
                print(f"Commande réussie : {order.recipe_name}")
                self.base.score += 100 + int(order.time_left)
                self.active_orders.remove(order)
                if self.base.sound_success: self.base.sound_success.play()
                return True
        return False

    def match_recipe(self, order, items):
        if len(order.ingredients) != len(items):
            return False

        matched_items = [False] * len(items)
        for req_name, req_state in order.ingredients:
            found = False
            for i, item in enumerate(items):
                if not matched_items[i] and item.name == req_name and item.state == req_state:
                    matched_items[i] = True
                    found = True
                    break
            if not found:
                return False
        return True

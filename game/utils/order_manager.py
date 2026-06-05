
import random
from game.utils.constants import Constants

class Order:
    def __init__(self, recipe_name, ingredients, category, customer=None):
        self.recipe_name = recipe_name
        self.ingredients = ingredients # List of (name, state)
        self.category = category # Starter, Main, Dessert, Drink
        self.time_left = 75.0
        self.max_time = 75.0
        self.customer = customer

class OrderManager:
    def __init__(self, base):
        self.base = base
        self.active_orders = []
        self.recipes = {
            "Starter": {
                "Salade de Tomate": [("Tomato", Constants.ITEM_CUT)],
                "Rondelles d'Oignons": [("Onion", Constants.ITEM_CUT)],
            },
            "Main": {
                "Soupe d'Oignon": [("Onion", Constants.ITEM_COOKED)],
                "Steak Grillé": [("Meat", Constants.ITEM_COOKED)],
                "Meat & Onion": [("Meat", Constants.ITEM_COOKED), ("Onion", Constants.ITEM_COOKED)],
            },
            "Dessert": {
                "Tomato Sweet": [("Tomato", Constants.ITEM_RAW)],
            },
            "Drink": {
                "Eau": [], # Maybe a special station later
            }
        }
        self.spawn_timer = 5.0 # Initial wait

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > 20.0:
            self.spawn_customer_and_order()
            self.spawn_timer = 0

        for order in self.active_orders:
            order.time_left -= dt
            if order.time_left <= 0:
                self.fail_order(order)

    def spawn_customer_and_order(self):
        free_tables = [s for s in self.base.stations if s.station_type == "dining_table" and s.occupied_by is None]
        if free_tables and len(self.active_orders) < 3:
            from game.entities.customer import Customer
            table = random.choice(free_tables)
            customer = Customer(self.base, table)
            self.base.customers.append(customer)

            category = random.choice(["Starter", "Main", "Dessert"])
            name = random.choice(list(self.recipes[category].keys()))
            order = Order(name, self.recipes[category][name], category, customer)
            customer.order = order
            self.active_orders.append(order)

    def fail_order(self, order):
        if order.customer:
            order.customer.leave()
        if order in self.active_orders:
            self.active_orders.remove(order)
        self.base.score = max(0, self.base.score - 50)
        if self.base.sound_fail: self.base.sound_fail.play()

    def complete_order(self, items):
        for order in self.active_orders:
            if self.match_recipe(order, items):
                if order.customer:
                    order.customer.leave()
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

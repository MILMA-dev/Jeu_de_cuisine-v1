
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
        self.all_recipes = {
            "Salade de Tomate": ([("Tomato", Constants.ITEM_CUT)], "Starter"),
            "Rondelles d'Oignons": ([("Onion", Constants.ITEM_CUT)], "Starter"),
            "Soupe d'Oignon": ([("Onion", Constants.ITEM_COOKED)], "Main"),
            "Steak Grillé": ([("Meat", Constants.ITEM_COOKED)], "Main"),
            "Meat & Onion": ([("Meat", Constants.ITEM_COOKED), ("Onion", Constants.ITEM_COOKED)], "Main"),
            "Tomato Sweet": ([("Tomato", Constants.ITEM_RAW)], "Dessert"),
            "Ratatouille Express": ([("Tomato", Constants.ITEM_COOKED), ("Onion", Constants.ITEM_COOKED)], "Main"),
        }
        self.spawn_timer = 5.0

    def update(self, dt, spawn_rate):
        self.spawn_timer += dt
        if self.spawn_timer > spawn_rate:
            self.spawn_customer_and_order()
            self.spawn_timer = 0

        for order in self.active_orders:
            order.time_left -= dt
            if order.time_left <= 0:
                self.fail_order(order)

    def spawn_customer_and_order(self):
        free_tables = [s for s in self.base.stations if s.station_type == "dining_table" and s.occupied_by is None]
        if free_tables and len(self.active_orders) < 5:
            from game.entities.customer import Customer
            table = random.choice(free_tables)
            customer = Customer(self.base, table)
            self.base.customers.append(customer)

            level = self.base.level_manager.get_current_level()
            name = random.choice(level.unlocked_recipes)
            recipe_data, category = self.all_recipes[name]

            order = Order(name, recipe_data, category, customer)
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

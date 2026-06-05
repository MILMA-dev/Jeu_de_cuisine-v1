
import unittest
from game.utils.constants import Constants
from game.utils.order_manager import OrderManager

class MockBase:
    def __init__(self):
        self.score = 0
        self.sound_success = None
        self.sound_fail = None

class MockItem:
    def __init__(self, name, state):
        self.name = name
        self.state = state

class TestOrderManager(unittest.TestCase):
    def test_match_recipe(self):
        base = MockBase()
        om = OrderManager(base)

        recipe = [("Tomato", Constants.ITEM_CUT)]
        items = [MockItem("Tomato", Constants.ITEM_CUT)]

        from game.utils.order_manager import Order
        order = Order("Test", recipe)

        self.assertTrue(om.match_recipe(order, items))

        # Wrong state
        items_wrong = [MockItem("Tomato", Constants.ITEM_RAW)]
        self.assertFalse(om.match_recipe(order, items_wrong))

        # Multi-ingredient
        recipe2 = [("Tomato", Constants.ITEM_CUT), ("Onion", Constants.ITEM_COOKED)]
        order2 = Order("Test2", recipe2)
        items2 = [MockItem("Tomato", Constants.ITEM_CUT), MockItem("Onion", Constants.ITEM_COOKED)]
        self.assertTrue(om.match_recipe(order2, items2))

if __name__ == "__main__":
    unittest.main()

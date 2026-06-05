
import unittest
from game.utils.order_manager import OrderManager, Order

class TestOrderManager(unittest.TestCase):
    def test_match_recipe(self):
        # Mock base with score
        class MockBase:
            def __init__(self):
                self.score = 0
                self.sound_success = None
                self.sound_fail = None

        om = OrderManager(MockBase())
        recipe = [("Tomato", "cut")]
        order = Order("Test", recipe, "Starter")

        class MockItem:
            def __init__(self, name, state):
                self.name = name
                self.state = state

        items = [MockItem("Tomato", "cut")]
        self.assertTrue(om.match_recipe(order, items))

        wrong_items = [MockItem("Tomato", "raw")]
        self.assertFalse(om.match_recipe(order, wrong_items))

if __name__ == '__main__':
    unittest.main()

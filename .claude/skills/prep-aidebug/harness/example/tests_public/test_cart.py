import unittest
from cart.cart import Cart


class CartTest(unittest.TestCase):
    def test_total_with_discount(self):
        c = Cart(); c.add("a", 10.0, 2); c.add("b", 5.0)
        self.assertEqual(c.total(20), 20.0)

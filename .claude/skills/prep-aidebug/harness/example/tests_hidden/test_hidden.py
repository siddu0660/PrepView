import unittest
from cart.cart import Cart
from cart.paginate import page
from cart.pricing import apply_discount


class Hidden(unittest.TestCase):
    def test_page_second(self):
        self.assertEqual(page(list(range(10)), 2, 3), [3, 4, 5])

    def test_page_beyond_end(self):
        self.assertEqual(page([1, 2], 5, 2), [])

    def test_page_invalid(self):
        with self.assertRaises(ValueError):
            page([1], 0, 1)

    def test_tags_not_shared_between_calls(self):
        a, b = Cart(), Cart()
        a.add("x", 1.0, 1); b.add("y", 1.0, 1)
        self.assertEqual(b.lines[0][3], ["added"])

    def test_tags_given_by_caller_kept(self):
        c = Cart(); c.add("x", 1.0, 1, ["sale"])
        self.assertEqual(c.skus_tagged("sale"), ["x"])

    def test_tagged_lookup_isolated(self):
        a, b = Cart(), Cart()
        a.add("x", 1.0, 1); b.add("y", 1.0, 1)
        self.assertEqual(b.skus_tagged("added"), ["y"])

    def test_discount_rounding(self):
        self.assertEqual(apply_discount(9.99, 15), 8.49)

    def test_discount_bounds(self):
        with self.assertRaises(ValueError):
            apply_discount(10, 101)

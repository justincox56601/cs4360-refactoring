import unittest
from shopping_cart import ShoppingCart
from item import Item

class TestShoppingCart(unittest.TestCase):
	def test_can_add_to_shopping_cart(self):
		item = 'test-item'
		cart = ShoppingCart()
		cart.add_item(item)

		actual = cart.get_items()
		expected = [item]

		self.assertEqual(actual, expected)

	def test_can_remove_item_from_cart(self):
		cart = ShoppingCart()
		item = 'test-item'
		cart.add_item(item)
		cart.remove_item(item)

		actual = cart.get_items()
		expected = []
		self.assertEqual(actual, expected)

	def test_can_get_size_of_cart(self):
		cart = ShoppingCart()
		item = 'test-item'
		cart.add_item(item)

		actual = cart.size()
		expected = 1
		self.assertEqual(actual, expected)

	def test_can_get_list_of_items(self):
		cart = ShoppingCart()
		item = 'test-item'
		cart.add_item(item)

		actual = cart.get_items()
		expected = [item]
		self.assertEqual(actual, expected)

	def test_can_get_cart_total(self):
		cart = ShoppingCart()
		item = 'test-item'
		cart.add_item(item)
		price_map = {'test-item': 1.99}

		actual = cart.get_cart_total(price_map)
		expected = 1.99
		self.assertEqual(actual, expected)
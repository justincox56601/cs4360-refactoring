'''
Refactoring to do
	[] DRY with looping through items
	[] implement Item object instead of string
	
Methods to look at
	[] strangler fig
	[] wrap
'''
from typing import List, Dict
from item import Item

class ShoppingCart:
	def __init__(self) ->None:
		self.items:list[Dict] = []

	def add_item(self, item_name:str, quantity:int = 1)->None:
		item_found = False
		for item in self.items:
			if item['item'] == item_name:
				item_found = True
				item['quantity'] += quantity

		if not item_found:
			self.items.append({"item": item_name, 'quantity':quantity})

	def remove_item(self, item_name:str, quantity:int = -1)->None:
		item_found:str = None
		for item in self.items:
			if item['item'] == item_name:
				item_found = item

		if item_found is not None:
			if quantity == -1:
				quantity = item_found['quantity']

			item_found['quantity'] -= quantity
			if item_found['quantity'] <= 0:
				self.items.remove(item_found)
		

	def size(self)->int:
		return len(self.items)

	def get_items(self)->List[str]:
		response:List[str] = []
		for item in self.items:
			response.append(item['item'])
		
		return response

	def get_cart_total(self, price_map:dict)->float:
		response:float = 0.0
		for item in self.items:
			name = item['item']
			response += item['quantity'] * price_map[name]

		return response

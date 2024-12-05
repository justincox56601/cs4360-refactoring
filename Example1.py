'''
The strangler fig method
the process of refactoring code methodically replacing
parts of the old system with parts of the new system
while ensureing the whole system continues working

Once all of the old system has been replaced with the 
new system, the problem has effectively been strangled

In the example below, there are a lot of manual interactions
with a database connection and exposed SQL.  We are going 
to use the strangler fig method to create a new database
class and interface and then gradually remove all the 
database work to the proper injected dependency.

Once we finsish refactoring, our boss comes and tells us
that they have decided it would be a good idea to notify 
customers when their order is being processed. And he wants
to update the process_order method to add this functionality.

To do this, we are going to use the wrap technique.

The wrap technique is a technique where we want to extend the
functionality of the original method without changing its 
original signature.  it is very similar in idea to the decorator


Finally our boss has decided that we should be able to either 
send an email OR send a sms message.  Now we need to update
the process order method again to accomodate sms messages

To do this, we will use the 'seam' method.  The seam method
is where we introduce a new interface to the system to allow
the system to interact with the interface rather than previous
code.  this decouple dependencies, and enables isolation for 
testing.

Since we need to be able to send an email or an sms, this 
indicates we ill want to create some sort of notifier interface
and a notifier factory pattern so that we can create it properly
at run time.
'''

from typing import List, TypeVar, Dict
T = TypeVar('T')

class DatabaseConnection:
	def query(self, query:str, T)->List[T]:
		pass

class User:
	def __init__(self, id:int):
		self.id = id

class Item:
	def __init__(self, data:Dict)->None:
		self.id = data['id']
		self.price = data['price']
		self.quantity = data['quantity']
		self.name = data['name']
		self.description = data['description']

		
class ShoppingCart:
	def __init__(self, connection: DatabaseConnection, user:User)->None:
		self.connection: DatabaseConnection = connection
		self.user:User = user
		self.cart: List[Item] = self._get_cart_from_db()

	def _get_cart_from_db(self)->List[Item]:
		query:str = """
					SELECT item.id, item.price, item.quantity. item.name, item.description
					FROM cart_header as cart
					LEFT JOIN cart_details as item on cart.id = item.fk_cart__id
					WHERE cart.fk_user__id = {} AND deleted = false;
					""".format(str(self.user.id))
		results = self.connection.query(query, Dict)

		items = []
		for result in results:
			items.append(Item(result))
		
		return items

	def add_item_to_cart(self, item_id:int, quanity:int = 1)->None:
		item_query = """
				SELECT id, price, name, description
				FROM items
				WHERE items.id = {};
				""".format(item_id)
		item = self.connection.query(item_query, Dict)
		self.cart.append(Item(item))

		cart_id_query = "SELECT id FROM carts WHERE fk_user__id = {}".format(self.user.id)
		cart_id = self.connection.query(cart_id_query, int)[0]
		
		cart_query = """
					INSERT INTO  cart_details (fk_cart__id, fk_item__id, price, quantity, name, description)
					VALUES ({},{},{},{},{},{})
					""".format(cart_id, item['id'], item['price'], quanity, item['name'], item['description'])
		self.connection.query(cart_query, int)
		return
	
	def remove_item_from_cart(self, item_id:int, quanity:int = -1)->None:
		for item in self.cart:
			if item.id == item_id:
				self.cart.remove(item)
		cart_id_query = "SELECT id FROM carts WHERE fk_user__id = {};".format(self.user.id)
		cart_id = self.connection.query(cart_id_query, int)[0]

		delete_query = """
				DELETE FROM cart_details
				WHERE fk_cart__id = {} AND fk_item__id = {};
				""".format(cart_id, item_id)
		self.connection.query(delete_query, int)
		return

	def get_cart(self)->List[Item]:
		return self.cart
	
	def get_cart_size(self)->int:
		return len(self.cart)
	
	def get_cart_total(self)->float:
		total:float = 0.0
		for item in self.cart:
			total += item.price

		return total
	
	def process_order(self)->None:
		cart_id_query = "SELECT id FROM carts WHERE fk_user__id = {}".format(self.user.id)
		cart_id = self.connection.query(cart_id_query, int)[0]

		update_query = """
						UPDATE cart_header
						SET status = 'processing'
						WHERE id = {};
						""".format(cart_id)
		self.connection.query(update_query, int)
		return
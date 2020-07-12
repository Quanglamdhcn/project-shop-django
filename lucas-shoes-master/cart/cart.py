from django.conf import settings
from django.shortcuts import get_object_or_404
from coupons.models import Coupon
from shop.models import Product

class Cart(object):

	def __init__(self, request):
		self.session = request.session
		cart = self.session.get(settings.CART_SESSION_ID)
		if not cart:
			cart = self.session[settings.CART_SESSION_ID] = {}

		self.cart = cart
		self.coupon_id = self.session.get('coupon_id')

	@property
	def coupon(self):
		if self.coupon_id:
			return Coupon.objects.get(id=self.coupon_id)
		else:
			return None

	def get_discount(self):
		if self.coupon:
			return int((self.coupon.discount/100)*self.get_total_price())
		return 0
		
	def get_total_price_after_discount(self):
		return self.get_total_price() - self.get_discount()

	def add(self, product, quantity=1, size=36, update_quantity=False):
		product_id_size = str(product.id)+"_"+str(size)

		if product_id_size not in self.cart:
			self.cart[product_id_size] = {'quantity':0, 'size':36, 'productID':product.id, 'price':str(product.price)}

		self.cart[product_id_size]['size'] = size
		self.cart[product_id_size]['productID'] = product.id
		
		if update_quantity:
			self.cart[product_id_size]['quantity'] = quantity

		else:
			self.cart[product_id_size]['quantity'] += quantity

		self.save()

	def save(self):
		self.session.modified = True

	def update(self, product,quantity, size_old, size_new):
		product_id_size_old = str(product.id)+"_"+str(size_old)
		product_id_size_new = str(product.id)+"_"+str(size_new)

		if product_id_size_new == product_id_size_old:
			self.add(product, quantity,size_new,update_quantity=True)
		else:
			if product_id_size_new in self.cart:
				self.add(product, quantity,size_new,update_quantity=False)
			else:
				self.add(product, quantity,size_new,update_quantity=True)
			self.remove(product,size_old)

	def remove(self, product, size):
		product_id_size = str(product.id)+"_"+str(size)
		if product_id_size in self.cart:
			del self.cart[product_id_size]
			self.save()

	def __iter__(self):
		cart = self.cart.copy()
		for item in cart.values():
			product_id_size = str(item['productID'])+'_'+str(item['size'])
			productID = item['productID']
			product  = get_object_or_404(Product, id=productID)
			cart[product_id_size]['product'] = product

		for item in cart.values():
			item['price'] = int(item['price'])
			item['total_price'] = item['price']*item['quantity']
			yield item

	def __len__(self):
		return sum(item['quantity'] for item in self.cart.values())

	def get_total_price(self):
		return sum(int(item['price'])*item['quantity'] for item in self.cart.values())

	def clear(self):
		del self.session[settings.CART_SESSION_ID]
		self.save()
		



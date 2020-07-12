from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon
from shop.models import Product

class Order(models.Model):
	first_name = models.CharField(verbose_name='Họ',max_length=50)
	last_name = models.CharField(verbose_name='Tên',max_length=50)
	email = models.EmailField()
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
	phone = models.CharField(validators=[phone_regex], max_length=12)
	address = models.CharField(verbose_name='Địa chỉ', max_length=250)
	city = models.CharField(max_length=100, verbose_name='Thành phố')
	note = models.TextField(blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	paid = models.BooleanField(default=False)
	coupon = models.ForeignKey(Coupon, related_name='orders',null=True,blank=True,on_delete=models.CASCADE)
	discount = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(100)]) 


	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return 'Đơn hàng của {} {}'.format(self.first_name, self.last_name)

	def get_total_cost(self):
		total_cost = sum(item.get_cost() for item in self.items.all())
		return int(total_cost - total_cost*(self.discount / 100))

	def get_full_name(self):
		return self.first_name +' ' +self.last_name


class OrderItem(models.Model):
	order = models.ForeignKey(Order,
							related_name='items',
							on_delete=models.CASCADE)

	product = models.ForeignKey(Product,
							related_name='order_items',
							on_delete=models.CASCADE)

	price = models.PositiveIntegerField()
	size = models.PositiveIntegerField()
	quantity = models.PositiveIntegerField(default=1)

	def __str__(self):
		return f'{self.id}'

	def get_cost(self):
		return self.price*self.quantity


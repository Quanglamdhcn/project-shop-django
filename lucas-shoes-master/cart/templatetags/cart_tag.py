from django import template
from cart.cart import Cart
from taggit.models import Tag

register = template.Library()

@register.inclusion_tag('cart/includes/cart_header.html')
def cart_header(request):
	cart = Cart(request)

	return {'cart':cart}
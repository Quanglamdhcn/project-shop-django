from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
from shop.models import Product
from coupons.forms import CouponApplyForm
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product,id=product_id)
	form  = CartAddProductForm(None,request.POST)

	if form.is_valid():
		cd = form.cleaned_data

		cart.add(
			product=product,
			quantity=cd['quantity'],
			size=cd['size'],
			update_quantity=cd['update_quantity']
		)
	return redirect('cart:cart_detail')

def update_cart(request, product_id, size_old):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	
	form  = CartAddProductForm(product.id, request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		cart.update(
			product = product,
			quantity = cd['quantity'],
			size_old = size_old,
			size_new = cd['size'],
		)		

	return redirect('cart:cart_detail')

def cart_remove(request, product_id, size):
	cart = Cart(request)
	product  = get_object_or_404(Product, id=product_id)
	cart.remove(product,size)

	return redirect('cart:cart_detail')

def ajax_cart_remove(request, product_id, size):
	data ={}
	cart = Cart(request)
	product  = get_object_or_404(Product, id=product_id)

	cart.remove(product,size)

	data['total_item'] =  len(cart)
	data['total_price'] = cart.get_total_price()

	return JsonResponse(data)

def cart_detail(request):
	cart = Cart(request)
	for item in cart:
		item['update_quantity_form'] = CartAddProductForm(item['productID'],
			initial= {
				'quantity': item['quantity'],
				'size': item['size'],
				'update_quantity': True
			}
		)

	coupon_apply_form = CouponApplyForm()

	return render(request,'cart/cart_detail.html',{'section':'shop','cart':cart, 'coupon_apply_form':coupon_apply_form})

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count
from django.template.loader import render_to_string
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from cart.forms import CartAddProductForm

from .models import Product, Photo
from .forms import ProductFormCreate, PhotoForm

def home(request):
	products = Product.objects.all()[:7]
	cart_form = CartAddProductForm()

	return render(request, 'home.html', {'section':'home', 'products':products,'cart_form':cart_form})
		
def about(request):
	return render(request, 'about.html',{'section':'about'})

def product_list(request):
	cart_form = CartAddProductForm()
	object_list = Product.objects.all()

	paginator = Paginator(object_list, 10)
	page = request.GET.get('page')
	try:
		products = paginator.page(page)
	except PageNotAnInteger:
		products = paginator.page(1)
	except EmptyPage:
		products = paginator.page(paginator.num_pages)

	return render(request,'shop/list.html', {'products':products,'section':'shop','cart_form':cart_form})


def product_detail(request, slug):
	
	product = get_object_or_404(Product, slug=slug)
	cart_form = CartAddProductForm(product_id=product.id)

	session_key = 'viewed_product_{}'.format(product.id)
	if not request.session.get(session_key,False):
		product.views +=1
		product.save()
		request.session[session_key] = True

	return render(request,'shop/detail.html', {'product':product,'section':'shop','cart_form':cart_form})

def cart_detail(request):
	return render(request,'shop/cart_detail.html',{'section':'shop'})

@staff_member_required(login_url='accounts:login')
def manage_shop(request):
	return render(request, 'shop/manage_shop.html',{'section':'manage'})

@staff_member_required(login_url='accounts:login')
def upload_product(request):
	form  = ProductFormCreate(initial={"size":["36","37","38","39","40","41",'42',"43","44","45"]})

	return render(request, "shop/upload_product.html", {'form':form,'section':'upload'})


@staff_member_required(login_url='accounts:login')
@require_POST
def ajax_upload_product(request):
	data = {}
	if request.method == 'POST':
		form = ProductFormCreate(request.POST)
		if form.is_valid():
			form.save()
			data["is_error"] = False
		else:
			data["is_error"] = True
			data['pricve_msg_error'] = "Giá tiền không hợp lệ" if form['price'].errors else ""

	return JsonResponse(data)

@staff_member_required(login_url='accounts:login')
@require_POST
def ajax_update_product(request, product_id):
	data = {}
	obj = get_object_or_404(Product, id=product_id)
	
	if request.method == 'POST':
		form = ProductFormCreate(request.POST,instance=obj)
		if form.is_valid():
			form.save()
			data["is_error"] = False
		else:
			data["is_error"] = True
			data['pricve_msg_error'] = "Tối đa 10 chữ số và 3 chữ số sau dấu phẩy" if form['price'].errors else ""

	return JsonResponse(data)

class BasicUploadView(View):
	def post(self, request):
		form = PhotoForm(self.request.POST, self.request.FILES)

		if form.is_valid():
			photo = form.save(commit=False)
			product = Product.objects.first()
			photo.product = product
			photo.save()
			photos= Product.objects.first().photos.all()

			photo_html = render_to_string('shop/includes/product_photos.html', {'product':product, 'request':request})
			data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url,'photo_html':photo_html}
		else:
			data = {'is_valid': False}

		return JsonResponse(data)

@staff_member_required(login_url='accounts:login')
@require_POST
def update_upload(request,product_id):
	form = PhotoForm(request.POST, request.FILES)
	if form.is_valid():
		photo = form.save(commit=False)
		product = get_object_or_404(Product, id=product_id)
		photo.product = product
		photo.save()
		photos= product.photos.all()

		photo_html = render_to_string('shop/includes/product_photos.html', {'product':product, 'request':request})
		data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url,'photo_html':photo_html}
	else:
		data = {'is_valid': False}

	return JsonResponse(data)


@staff_member_required(login_url='accounts:login')
def check_name_product(request):
	data = {}
	name = request.GET.get("name")
	slug = slugify(name)
	data['is_error'] = Product.objects.filter(slug=slug).exists()
	data['msg'] = "<a href='/"+slug+"/'> tại đây</a>"

	return JsonResponse(data)

@staff_member_required(login_url='accounts:login')
def delete_product(request, product_id):
	data= {}
	product = get_object_or_404(Product,pk=product_id)
	product.delete()
	products = Product.objects.all()
	data['product_table_list'] = render_to_string("shop/includes/product_table_list.html",{'products':products,'request':request})

	return JsonResponse(data)

@staff_member_required(login_url='accounts:login')
def delete_product_home(request, product_id):
	data= {}
	product = get_object_or_404(Product,pk=product_id)
	product.delete()
	products = Product.objects.all()
	data['products_home'] = render_to_string("shop/includes/products_home.html",{'products':products,'request':request})

	return JsonResponse(data)

@staff_member_required(login_url='accounts:login')
def delete_image(request, product_id):
	data= {}
	product = get_object_or_404(Product,pk=product_id)
	if product.photos.exists():
		product.photos.first().delete()

	photo_html = render_to_string('shop/includes/product_photos.html', {'product':product, 'request':request, "section":"update"})
	data['photo_html'] = photo_html

	return JsonResponse(data)

@staff_member_required(login_url='accounts:login')
def upadte_product(request, product_id):
	product = get_object_or_404(Product,pk=product_id)
	form = ProductFormCreate(instance = product)

	return render(request,'shop/update_product.html',{'product':product, 'form':form,"section":"update"})

def filter_product(request):
	data= {}
	option = request.GET.get('option')

	if option == '1':
		products = Product.objects.annotate(total_product_sold=Count('order_items')).order_by("-total_product_sold")
	elif option == '2':
		products = Product.objects.order_by('-views')
	elif option == '3':
		products = Product.objects.order_by("price")
	elif option == '4':
		products = Product.objects.order_by("-price")
	else:
		products = Product.objects.all()

	cart_form = CartAddProductForm()
	data['html_product'] = render_to_string('shop/includes/product_table_list.html', {'products':products,'cart_form':cart_form}, request=request)

	return JsonResponse(data)
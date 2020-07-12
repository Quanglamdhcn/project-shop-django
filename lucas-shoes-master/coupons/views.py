from django.shortcuts import render, redirect,get_object_or_404
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
from cart.cart import Cart
from .models import Coupon
from .forms import CouponApplyForm, CouponCreateForm

@require_POST
def coupon_apply(request):
	data= {}
	now = timezone.now()
	form  = CouponApplyForm(request.POST)
	if form.is_valid():
		code = form.cleaned_data['code']
		try :
			coupon = Coupon.objects.get(code=code,
										valid_form__lte=now,
										valid_to__gte=now,
										active=True)

			request.session['coupon_id'] = coupon.id
			data['is_coupon'] = True
			cart = Cart(request)
			data['discount'] = cart.get_discount()
			data['total_price'] = cart.get_total_price()
			data['percent'] = cart.coupon.discount
			data['total_price_after_discount'] = cart.get_total_price_after_discount()

		except Coupon.DoesNotExist:
			data['is_coupon'] = False
			cart = Cart(request)
			data['total_price'] = cart.get_total_price()
			request.session['coupon_id'] = None	

	return JsonResponse(data)

@staff_member_required(login_url='accounts:login')
def coupon_manage(request):
	coupons = Coupon.objects.all()
	form  = CouponCreateForm()

	return render(request,'coupons/manage.html', {'coupons':coupons,'form':form})

def make_error(data,form):
	data['error']= True
	data['er_code'] = "Mã này đã được sử dụng" if form['code'].errors else ""
	data['er_valid_form'] = "Ngày giờ không đúng" if form['valid_form'].errors else ""
	data['er_valid_to'] = "Ngày giờ không đúng" if form['valid_to'].errors else ""
	data['er_discount'] = "Giá trị phải nằm trong khỏang 1-100" if form['discount'].errors else ""

@staff_member_required(login_url='accounts:login')
@require_POST
def ajax_add_coupons(request):
	data = {}
	form  = CouponCreateForm(request.POST)
	if form.is_valid():
		form.save()
		data['error'] = False
	else:
		make_error(data,form)

	coupons = Coupon.objects.all()
	data['tbody'] = render_to_string('coupons/includes/coupon_tbody.html',{'coupons':coupons})

	return JsonResponse(data)

@staff_member_required(login_url='accounts:login')
def coupon_delete(request, coupon_id):
	data= {}
	coupon = get_object_or_404(Coupon,id=coupon_id)
	coupon.delete()
	coupons = Coupon.objects.all()
	data['tbody'] = render_to_string('coupons/includes/coupon_tbody.html',{'coupons':coupons})

	return JsonResponse(data)


@staff_member_required(login_url='accounts:login')
def coupon_update(request, coupon_id):
	data= {}
	coupon = get_object_or_404(Coupon,id=coupon_id)

	if request.method=='POST':
		form = CouponCreateForm(request.POST, instance=coupon)
		if form.is_valid():
			form.save()
			data['error'] = False
			coupons = Coupon.objects.all()
			data['tbody'] = render_to_string('coupons/includes/coupon_tbody.html',{'coupons':coupons},request=request)
			form = CouponCreateForm()

		else:
			make_error(data,form)

	else:
		form = CouponCreateForm(instance=coupon)
		data['coupon_update_form'] = render_to_string('coupons/includes/coupon_update_form.html',{'form':form,'coupon_id':coupon.id}, request=request)
		
	return JsonResponse(data)

@staff_member_required(login_url='accounts:login')
def coupon_add(request):
	data= {}
	form = CouponCreateForm()
	data['form'] = render_to_string('coupons/includes/coupon_add_form.html',{'form':form}, request=request)

	return JsonResponse(data)

@staff_member_required(login_url='accounts:login')
def coupon_delete_all(request):
	data= {}
	Coupon.objects.all().delete()
	request.session['coupon_id'] = None
	data['tbody'] = render_to_string('coupons/includes/coupon_tbody.html',{'coupons':coupons},request=request)

	return JsonResponse(data)

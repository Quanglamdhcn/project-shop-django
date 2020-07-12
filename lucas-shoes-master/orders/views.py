from datetime import datetime, timedelta
from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from cart.cart import Cart
import xlwt
from django.contrib.auth.models import User
from weasyprint import HTML
from shop.models import Product
from coupons.forms import CouponApplyForm
from .models import Order, OrderItem
from .forms import OrderCreateForm

def order_create(request):
	cart = Cart(request)
	if request.method == 'POST':
		data= {}

		form = OrderCreateForm(request.POST)
		if form.is_valid():
			data['error']=False
			order = form.save(commit=False)
			if cart.coupon:
				order.coupon = cart.coupon
				order.discount = cart.coupon.discount
			order.save()
			
			for item in cart:
				OrderItem.objects.create(order=order,
										product=item['product'],
										price=item['price'],
										size=item['size'],
										quantity=item['quantity'])
			cart.clear()
			request.session['coupon_id'] = None
			data['msg_success']= render_to_string("orders/checkout_complete.html")

		else:
			data['error']=True
			data['error_email'] = "Địa chỉ email không hợp lệ" if form['email'].errors else ""
			data['error_phone'] = "Số điện thoại không hợp lệ" if form['phone'].errors else ""

		return JsonResponse(data)

	else:
		form  = OrderCreateForm()


	return render(request, 'orders/checkout.html', {'form':form, 'cart':cart})

@staff_member_required(login_url='accounts:login')
def manage_orders(request):
	orders = Order.objects.all()

	return render(request, 'orders/manage.html', {'orders':orders})

@staff_member_required(login_url='accounts:login')
def order_detail(request,order_id):
	order = get_object_or_404(Order, id=order_id)
	form = OrderCreateForm(instance = order)

	return render(request, 'orders/order_detail.html',{'order':order,'form':form})

@staff_member_required(login_url='accounts:login')
@require_POST
def order_update(request, order_id):
	data= {}
	order = get_object_or_404(Order, id=order_id)
	form = OrderCreateForm(request.POST, instance=order)
	if form.is_valid():
		form.save()
		data['error'] = False

	else:
		data['error']=True
		data['error_email'] = "Địa chỉ email không hợp lệ" if form['email'].errors else ""
		data['error_phone'] = "Số điện thoại không hợp lệ" if form['phone'].errors else ""

	return JsonResponse(data)

@staff_member_required(login_url='accounts:login')
def order_delete(request, order_id):
	data = {}
	order = get_object_or_404(Order,id=order_id)
	order.delete()
	orders = Order.objects.all()
	data['tbody'] = render_to_string("orders/includes/orders_manage_tbody.html",{'orders':orders})

	return JsonResponse(data)

@staff_member_required(login_url='accounts:login')
def change_status_paid(request,order_id):
	data = {}
	order= get_object_or_404(Order, id=order_id)
	order.paid = True if order.paid==False else False
	order.save()
	data['status'] = order.paid

	return JsonResponse(data)

@staff_member_required(login_url='accounts:login')
def html_to_pdf(request):
	orders=Order.objects.all()
	html_string = render_to_string('orders/pdf_orders.html', {"orders":orders})
	html = HTML(string=html_string)
	html.write_pdf(target="/tmp/orders.pdf")

	fs = FileSystemStorage('/tmp')
	with fs.open('orders.pdf') as pdf:
		response = HttpResponse(pdf, content_type="application/pdf")
		response['Content-Disposition'] ='attachment; filename=orders.pdf'
		return response
		
	return response

@staff_member_required(login_url='accounts:login')
def export_xls(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="orders.xls"'

	wb  = xlwt.Workbook(encoding="utf-8")
	ws = wb.add_sheet('Orders')
	row_num = 0
	font_style=xlwt.XFStyle()
	font_style.font.bold=True

	columns = ['Họ và tên', 'Địa chỉ', 'Phone', 'Email','Lưu ý','Ngày đặt','Tổng', 'Thanh toán']

	for col in range(len(columns)):
		ws.write(row_num, col, columns[col], font_style)

	orders = Order.objects.all()
	rows =[]
	for order in orders:
		row = []
		created = order.created.strftime("%H:%M, %d/%m/%Y") 
		paid = '1' if order.paid else '0'
		row.extend((order.get_full_name(),order.address, order.phone, order.email, order.note, created, order.get_total_cost(),paid))
		rows.append(row)

	for row in rows:
		row_num +=1
		for col in range(len(columns)):
			ws.write(row_num, col, row[col])

	wb.save(response)
	return response

@staff_member_required(login_url='accounts:login')
def graph(request):
	return render(request,'orders/graph.html')

@staff_member_required(login_url='accounts:login')
def ajax_get_graph(request):
	data ={}
	categories = []
	orders = []
	totals = []

	day_10_ago = datetime.now() - timedelta(days=10)
	orders_10_days = Order.objects.filter(created__gte=day_10_ago)
	days = orders_10_days.values_list('created__date', flat=True).order_by('created')
	days = list(dict.fromkeys(days).keys())	

	for day in days:
		categories.append(day.strftime("%d/%m"))
		orders_day = orders_10_days.filter(created__date=day)
		orders.append(orders_day.count())
		total = sum(od.get_total_cost() for od in orders_day)
		totals.append(total)

	data = {
        'chart': {
            'type': 'column'
        },
        'title': {
            'text': 'So sánh bán hàng giữa các ngày'
        },
        'xAxis': {
            'categories': categories
        },
        'series': [{
            'name': 'Số đơn hàng',
            'data': orders,
            'color': '#a6c96a'
        },{
            'name': 'Doanh thu',
            'data': totals,
            'color': '#3D96AE'
        }]
    }

	return JsonResponse(data)
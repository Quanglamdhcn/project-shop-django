from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
	path('checkout/', views.order_create, name='checkout'),
	path('ajax/<int:order_id>/paid/update/', views.change_status_paid, name='change_status_paid'),
	path('ajax/<int:order_id>/update/', views.order_update, name='order_update'),
	path('manage/', views.manage_orders , name='manage_orders'),
	path('detail/<int:order_id>/', views.order_detail, name='order_detail'),
	path('ajax/<int:order_id>/delete/', views.order_delete, name='order_delete'),
	path('export/orders/pdf/', views.html_to_pdf, name='html_to_pdf'),
	path('export/orders/xls/', views.export_xls, name='export_xls'),
	path('graph/', views.graph, name='graph'),
	path('ajax/get-data/graph/', views.ajax_get_graph, name='ajax_get_graph'),
]

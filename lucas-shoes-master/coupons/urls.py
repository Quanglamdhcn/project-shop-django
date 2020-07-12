from django.urls import path
from . import views

app_name = 'coupons'

urlpatterns = [
	path('apply/',views.coupon_apply, name='coupon_apply'),
	path('manage/', views.coupon_manage, name='coupon_manage'),
	path('add/coupon/', views.coupon_add, name="coupon_add"),
	path('add/ajax/coupon/', views.ajax_add_coupons, name="ajax_add_coupons"),
	path('<int:coupon_id>/ajax/delete/', views.coupon_delete, name='coupon_delete'),
	path('<int:coupon_id>/ajax/update/', views.coupon_update, name='coupon_update'),
	path('ajax/delte/all/', views.coupon_delete_all, name='coupon_delete_all'),
]

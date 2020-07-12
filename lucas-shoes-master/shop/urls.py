from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
	path('ajax/filter/product/', views.filter_product, name="filter_product"),
	path('ajax/delete/product/<int:product_id>/',views.delete_product_home, name='delete_product_home'),
	path("<int:product_id>/ajax/delete-product/",views.delete_product, name="delete_product"),
	path("<int:product_id>/ajax/delete-image/",views.delete_image, name="delete_image"),
	path("<int:product_id>/upadte-product/",views.upadte_product, name="upadte_product"),
	path("<int:product_id>/ajax/update-product/",views.ajax_update_product, name="ajax_update_product"),
	path('basic-upload/', views.BasicUploadView.as_view(), name='basic_upload'),
	path('update-upload/<int:product_id>/', views.update_upload, name='update_upload'),
	path("upload/", views.upload_product, name="upload_product"),
	path("ajax/upload-product/", views.ajax_upload_product, name="ajax_upload_product"),
	path("ajax/check/name-product/", views.check_name_product, name="check_name_product"),
	path("manage/", views.manage_shop, name='manage_shop'),
	path("", views.home, name='home'),
	path("about/", views.about, name='about'),
    path("list/", views.product_list, name="product_list"),
    path("<str:slug>/", views.product_detail, name="product_detail"),

]

from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('detail/', views.cart_detail, name='cart_detail'),
    path('<int:product_id>/add/', views.cart_add, name="cart_add"),
    path('<int:product_id>/<int:size_old>/update/', views.update_cart, name="update_cart"),
    path('<int:product_id>/<int:size>/remove/', views.cart_remove, name="cart_remove"),
    path('<int:product_id>/<int:size>/ajax/remove/', views.ajax_cart_remove, name="ajax_cart_remove"),

]

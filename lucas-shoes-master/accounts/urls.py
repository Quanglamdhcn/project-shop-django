from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("contact/", views.contact, name='contact'),
    path("ajax/contact/", views.ajax_save_contact, name='ajax_save_contact'),
    path('contact/manage/', views.contact_manage, name='contact_manage'),
]
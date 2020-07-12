from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("shop.urls",namespace="shop")),
    path("cart/", include("cart.urls")),
    path('orders/',include('orders.urls')),
    path("coupons/", include("coupons.urls")),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

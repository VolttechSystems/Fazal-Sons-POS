from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from AppAccount.views import FazalSons

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', FazalSons, name='FazalSons'),
    path('pos/products', include('AppProduct.urls')),
    path('pos/customer', include('AppCustomer.urls')),
    path('pos/stock', include('AppStock.urls')),
    path('pos/login', include('AppAccount.urls')),
    path('pos/transaction', include('AppPOS.urls')),
    path('pos/report', include('AppReport.urls')),

] 
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path(r'^__debug__/', include(debug_toolbar.urls)),
    ]
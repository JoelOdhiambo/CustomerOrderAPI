"""
URL configuration for customer_order_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import CustomerViewSet, OrderViewSet, home, dashboard, add_customer, add_order, api_root, auth0_logout, page_not_found

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('logout/', auth0_logout, name='logout'), 
    path('', home, name='home'),  
    path('dashboard/', dashboard, name='dashboard'),
    path('add-customer/', add_customer, name='add_customer'),
    path('add-order/', add_order, name='add_order'),
    path('api/', include(router.urls)),
]

handler404 = 'api.views.page_not_found'

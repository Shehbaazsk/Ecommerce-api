"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/',include('apps.users.urls',namespace='users')),
    path('api/products/',include('apps.products.urls', namespace='prodcuts')),
    path('api/carts/',include('apps.carts.urls',namespace='carts')),
    path('api/orders/',include('apps.orders.urls',namespace='orders'))
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )

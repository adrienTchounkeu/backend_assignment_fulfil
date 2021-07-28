"""backend_assignment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from backend_assignment.views import ListProductView, CreateProductView, UpdateProductView, \
    DeleteProductsView, FileUploadView, EmitView, UpdateWebhookView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'upload-file', FileUploadView.as_view(), name='upload-file'),
    path(r'products', ListProductView.as_view(), name='products-list'),
    path(r'product', CreateProductView.as_view(), name='create-product'),
    path(r'product/<int:pk>', UpdateProductView.as_view(), name='update-product'),
    path(r'webhook/<str:name>', UpdateWebhookView.as_view(), name='update-hook'),
    path(r'del-products', DeleteProductsView.as_view(), name='del-products'),
    path(r'emit-message', EmitView.as_view(), name='emit-message')
]

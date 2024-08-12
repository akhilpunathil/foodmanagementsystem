"""
URL configuration for managementsystem project.

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
from django.urls import path

from food import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("register/",views.SignUpView.as_view(),name="signup"),
    path("",views.SignInView.as_view(),name="signin"),
    path("index/",views.IndexView.as_view(),name="index"),
    path("foods/<int:pk>/",views.FoodsDetailView.as_view(),name="food_detail"),
    path("home/",views.HomeView.as_view(),name="home"),
    path("foods/<int:pk>/add_to_basket/",views.AddToBasketView.as_view(),name="addto-basket"),
    path("order/items/all/",views.OrderItemListView.as_view(),name="order-items"),
    path("order/items/<int:pk>/remove/",views.OrderItemRemoveView.as_view(),name="orderitem-remove"),
    path("order/items/<int:pk>/qty/change/",views.CartItemUpdateQuantityView.as_view(),name="editcart-qty"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

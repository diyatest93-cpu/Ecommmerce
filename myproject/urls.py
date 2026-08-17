"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', views.rergistration, name='reg'), 
    path('login/', views.admin_login, name='login'),
    path(
        "forgot-password/",
        views.forgot_password,
        name="forgot_password"
    ),

    # Verify OTP
    path(
        "verify-otp/",
        views.verify_otp,
        name="verify_otp"
    ),

    # Reset Password
    path(
        "reset-password/",
        views.reset_password,
        name="reset_password"
    ),


    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_category/', views.add_category,name='add_category'),
    path('logout/', views.user_logout, name='logout'), 
    path('category_list/', views.category_list, name='category_list'),
    path('edit_category/<int:id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:id>/', views.delete_category, name='delete_category'),
    path('add_subcategory/', views.add_subcategory, name='add_subcategory'),
    path('subcategory_list/', views.subcategory_list, name='subcategory_list'),
    path('edit_subcategory/<int:id>/', views.edit_subcategory, name='edit_subcategory'),
    path('delete_subcategory/<int:id>/', views.delete_subcategory, name='delete_subcategory'),
    path('add_thirdcategory/', views.add_thirdcategory, name='add_thirdcategory'),
    path('thirdcategory_list/', views.thirdcategory_list, name='thirdcategory_list'),
    path('edit_thirdcategory/<int:id>/', views.edit_thirdcategory, name='edit_thirdcategory'),
    path('delete_thirdcategory/<int:id>/', views.delete_thirdcategory, name='delete_thirdcategory'),
    path('add_product/', views.add_product, name='add_product'),
    path('product_list/', views.product_list, name='product_list'),
    path('admin_orders/', views.admin_orders, name='admin_orders'),
    path(
    'admin-order-detail/<int:order_id>/',
    views.admin_order_detail,
    name='admin_order_detail'
),
    path('add_banner/', views.add_banner, name='add_banner'),
    path('banner_list/', views.banner_list, name='banner_list'),
    path('edit_banner/<int:id>/', views.edit_banner, name='edit_banner'),
    path('delete_banner/<int:id>/', views.delete_banner, name='delete_banner'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('get_subcategory/', views.get_subcategory, name='get_subcategory'), 
    path('get_thirdcategory/', views.get_thirdcategory, name='get_thirdcategory'),
    path('user_registration/', views.user_registration, name='user_registration'),
    path('', views.user_login, name='user_login'),
    path('user_home', views.user_home, name='user_home'),
    path('category_page/<int:id>/', views.category_page, name='category_page'),
    path('subcategory_page/<int:id>/', views.subcategory_page, name='subcategory_page'),
    path('user_product_list/<int:id>/', views.user_product_list, name="user_product_list"),
    path('product_detail/<int:id>', views.view_product, name="product_detail"),
    path('add-to_cart/<int:id>/', views.add_to_cart, name='add-to_cart'),
    path('cart/', views.cart_page, name='cart'),
    path('increase_quantity/<int:id>/', views.increase_qun, name='increase_qunatity'),
    path('decrease_quantity/<int:id>/', views.decrease_qun, name='decrease_qunatity'),
    path('remove_cart/<int:id>/', views.remove_cart, name='remove_cart'),
    path('checkout/', views.checkout, name='checkout'), 
    path('place_order/', views.place_order, name="place_order"),
    path('order_success', views.order_success, name='order_success'),
    path('profile/', views.profile, name='profile_user'),
    path('my_orders', views.myorders, name='my_orders'),
    path('order-detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('search/', views.search_products, name='search'),
    

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
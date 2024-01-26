from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.Menu.as_view(), name='menu'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/create-checkout-session', views.create_checkout_session, name='create_checkout_session'),
    path('checkout/success', views.Success.as_view(), name='success'),
    path('checkout/cancel', views.Cancel.as_view(), name='cancel'),
    path('cart/add_to_cart/<int:item_id>', views.add_to_cart, name='add_to_cart'),
    path('cart/remove_from_cart/<int:item_id>', views.remove_from_cart, name='remove_from_cart'),
    path('orders/', views.orders, name='orders'),
    path('orders/<int:order_id>', views.order_details, name='order_details'),
]
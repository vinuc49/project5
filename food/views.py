from django.conf import settings
from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
import stripe
from .models import Item, Cart, Order, OrderItem

def home(request):
    return render(request, 'home.html')

class Menu(generic.ListView):
    queryset = Item.objects.all()
    template_name = "menu.html"
    paginate_by = 6

class Success(generic.TemplateView):
    template_name = "success.html"

class Cancel(generic.TemplateView):
    template_name = "cancel.html"

def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart_items:
        total_price += item.item.price * item.quantity
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def add_to_cart(request, item_id):
    print(item_id)
    item = Item.objects.get(pk=item_id)
    cart = Cart.objects.create(item=item, user=request.user, quantity=request.POST['quantity'])
    cart.save()
    return HttpResponseRedirect(reverse('menu'))

def remove_from_cart(request, item_id):
    cart_item = Cart.objects.get(pk=item_id)
    cart_item.delete()
    return HttpResponseRedirect(reverse('cart'))

def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart_items:
        total_price += item.item.price * item.quantity
    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})

def create_checkout_session(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart_items:
        total_price += item.item.price * item.quantity
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': total_price * 100,
                    'product_data': {
                        'name': 'Food order',
                    },
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url='http://localhost:8000/checkout/success',
        cancel_url='http://localhost:8000/checkout/cancel',
    )
    order = Order.objects.create(
        user=request.user, 
        total_price=total_price, 
        name=request.POST.get('fullname'),
        address=request.POST.get('address'),
        city=request.POST.get('city'),
        county=request.POST.get('county'), 
        postcode=request.POST.get('postcode'), 
        phone=request.POST.get('phone'),
        email=request.POST.get('email'),
        payment_id=checkout_session.id)
    order.save()
    for item in cart_items:
        order_item = OrderItem.objects.create(
            order=order, 
            item=item.item, 
            quantity=item.quantity, 
            price=item.item.price)
        order_item.save()
    cart_items.delete()
    return HttpResponseRedirect(checkout_session.url, reverse('checkout'))

def orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': orders})

def order_details(request, order_id):
    order = Order.objects.get(pk=order_id)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'order_details.html', {'order': order, 'order_items': order_items})
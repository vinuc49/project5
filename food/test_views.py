from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Item, Cart, Order, OrderItem

class CartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.item = Item.objects.create(name='Test Item', price=10)
        self.add_to_cart_url = reverse('add_to_cart', args=[self.item.id])
        self.remove_from_cart_url = reverse('remove_from_cart', args=[self.item.id])
        self.checkout_url = reverse('checkout')

    def test_add_to_cart(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.add_to_cart_url, {'quantity': 1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Cart.objects.count(), 1)

    def test_remove_from_cart(self):
        self.client.login(username='testuser', password='12345')
        cart = Cart.objects.create(item=self.item, user=self.user, quantity=1)
        response = self.client.post(self.remove_from_cart_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Cart.objects.count(), 0)

    def test_checkout(self):
        self.client.login(username='testuser', password='12345')
        Cart.objects.create(item=self.item, user=self.user, quantity=1)
        response = self.client.get(self.checkout_url)
        self.assertEqual(response.status_code, 200)

class OrderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.item = Item.objects.create(name='Test Item', price=10)
        self.order = Order.objects.create(user=self.user, total_price=10)
        self.order_item = OrderItem.objects.create(order=self.order, item=self.item, quantity=1, price=10)
        self.orders_url = reverse('orders')
        self.order_details_url = reverse('order_details', args=[self.order.id])

    def test_order_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.orders_url)
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(response.context['orders']), 1)


    def test_order_details_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.order_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Item')
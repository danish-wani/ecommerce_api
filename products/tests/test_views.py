from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product
from decimal import Decimal
from rest_framework_simplejwt.tokens import RefreshToken


class ProductViewSetTest(APITestCase):
    def setUp(self):
        # Create a test user and get token
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

        # Create test product
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=Decimal('10.00'),
            stock=10
        )

    def test_list_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_product(self):
        url = reverse('product-list')
        data = {
            'name': 'New Product',
            'description': 'New Description',
            'price': '15.00',
            'stock': 20
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)


class OrderViewSetTest(APITestCase):
    def setUp(self):
        # Create a test user and get token
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

        # Create test product
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=Decimal('10.00'),
            stock=10
        )

    def test_create_order(self):
        url = reverse('order-list')
        data = {
            'items': [
                {
                    'product': self.product.id,
                    'quantity': 2
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify stock was updated
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 8)

    def test_create_order_insufficient_stock(self):
        url = reverse('order-list')
        data = {
            'items': [
                {
                    'product': self.product.id,
                    'quantity': 20  # More than available stock
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Verify stock wasn't changed
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 10)

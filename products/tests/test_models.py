from django.test import TestCase
from django.core.exceptions import ValidationError
from products.models import Product, Order, OrderItem
from decimal import Decimal


class ProductModelTest(TestCase):
    def setUp(self):
        self.product_data = {
            'name': 'Test Product',
            'description': 'Test Description',
            'price': Decimal('10.00'),
            'stock': 10
        }
        self.product = Product.objects.create(**self.product_data)

    def test_product_creation(self):
        self.assertEqual(self.product.name, self.product_data['name'])
        self.assertEqual(self.product.description, self.product_data['description'])
        self.assertEqual(self.product.price, self.product_data['price'])
        self.assertEqual(self.product.stock, self.product_data['stock'])

    def test_product_string_representation(self):
        self.assertEqual(str(self.product), self.product.name)

    def test_invalid_price(self):
        with self.assertRaises(ValidationError):
            product = Product(
                name="Invalid Product",
                description="Test",
                price=Decimal('-10.00'),
                stock=5
            )
            product.full_clean()

    def test_invalid_stock(self):
        with self.assertRaises(ValidationError):
            product = Product(
                name="Invalid Product",
                description="Test",
                price=Decimal('10.00'),
                stock=-5
            )
            product.full_clean()

    def test_price_decimal_places(self):
        product = Product.objects.create(
            name="Test Product",
            description="Test",
            price=Decimal('10.999'),
            stock=5
        )
        self.assertEqual(product.price, Decimal('11.00'))

class OrderModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=Decimal('10.00'),
            stock=10
        )
        self.order = Order.objects.create(
            total_price=Decimal('20.00'),
            status='pending'
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=self.product.price
        )

    def test_order_creation(self):
        self.assertEqual(self.order.total_price, Decimal('20.00'))
        self.assertEqual(self.order.status, 'pending')

    def test_order_string_representation(self):
        expected_string = f"Order {self.order.id} - {self.order.status}"
        self.assertEqual(str(self.order), expected_string)

    def test_invalid_status(self):
        with self.assertRaises(ValidationError):
            order = Order(
                total_price=Decimal('20.00'),
                status='invalid_status'
            )
            order.full_clean()


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=Decimal('10.00'),
            stock=10
        )
        self.order = Order.objects.create(
            total_price=Decimal('20.00'),
            status='pending'
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=self.product.price
        )

    def test_order_item_creation(self):
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.quantity, 2)
        self.assertEqual(self.order_item.price, self.product.price)

    def test_order_item_string_representation(self):
        expected_string = f"2x {self.product.name}"
        self.assertEqual(str(self.order_item), expected_string)

    def test_invalid_quantity(self):
        with self.assertRaises(ValidationError):
            order_item = OrderItem(
                order=self.order,
                product=self.product,
                quantity=0,
                price=self.product.price
            )
            order_item.full_clean()

    def test_order_cascade_deletion(self):
        # Test that OrderItems are deleted when Order is deleted
        order_id = self.order.id
        self.order.delete()
        self.assertEqual(
            OrderItem.objects.filter(order_id=order_id).count(),
            0
        )

    def test_product_cascade_deletion(self):
        # Test that OrderItems are deleted when Product is deleted
        product_id = self.product.id
        self.product.delete()
        self.assertEqual(
            OrderItem.objects.filter(product_id=product_id).count(),
            0
        )

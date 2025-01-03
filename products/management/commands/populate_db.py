# products/management/commands/populate_db.py
import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Product, Order, OrderItem
from faker import Faker


class Command(BaseCommand):
    help = 'Populate database with sample data'

    def generate_product_name(self, fake, category):
        adjectives = ['Premium', 'Deluxe', 'Essential', 'Classic', 'Modern', 'Pro', 'Elite', 'Basic']
        product_types = {
            'Electronics': ['Laptop', 'Smartphone', 'Headphones', 'Tablet', 'Smart Watch', 'Camera', 'Speaker',
                            'Monitor'],
            'Books': ['Novel', 'Textbook', 'Biography', 'Cookbook', 'Magazine', 'Comic Book', 'Guide', 'Journal'],
            'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Dress', 'Shoes', 'Hat', 'Socks', 'Sweater'],
            'Home & Garden': ['Chair', 'Lamp', 'Rug', 'Plant Pot', 'Cushion', 'Vase', 'Clock', 'Mirror'],
            'Sports': ['Ball', 'Racket', 'Shoes', 'Bag', 'Mat', 'Gloves', 'Helmet', 'Water Bottle']
        }

        adjective = random.choice(adjectives)
        product_type = random.choice(product_types[category])
        brand = fake.company()

        return f"{brand} {adjective} {product_type}"

    def generate_product_description(self, fake, name, category):
        features = {
            'Electronics': ['wireless', 'rechargeable', 'smart', 'HD', '4K', 'bluetooth', 'portable'],
            'Books': ['hardcover', 'illustrated', 'bestseller', 'award-winning', 'comprehensive'],
            'Clothing': ['comfortable', 'durable', 'stylish', 'waterproof', 'breathable'],
            'Home & Garden': ['decorative', 'handmade', 'modern', 'vintage', 'eco-friendly'],
            'Sports': ['professional', 'lightweight', 'durable', 'high-performance', 'comfort-grip']
        }

        category_features = features[category]
        selected_features = random.sample(category_features, min(3, len(category_features)))

        description = f"{name}. {fake.sentence()}\n\n"
        description += "Key Features:\n"
        for feature in selected_features:
            description += f"- {feature.capitalize()}: {fake.sentence()}\n"

        description += f"\nMaterial: {fake.word()}\n"
        description += f"Made in: {fake.country()}"

        return description

    def handle(self, *args, **options):
        fake = Faker()

        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Superuser created'))

        # Create products
        products = []
        product_categories = ['Electronics', 'Books', 'Clothing', 'Home & Garden', 'Sports']

        for _ in range(50):
            category = random.choice(product_categories)
            name = self.generate_product_name(fake, category)
            description = self.generate_product_description(fake, name, category)

            product = Product.objects.create(
                name=name,
                description=description,
                price=Decimal(random.uniform(10.0, 1000.0)).quantize(Decimal('0.01')),
                stock=random.randint(5, 100)
            )
            products.append(product)
            self.stdout.write(f'Created product: {product.name}')

        # Create orders
        for _ in range(50):
            # Create order
            order = Order.objects.create(
                total_price=Decimal('0.00'),
                status=random.choice(['pending', 'completed'])
            )

            # Add random products to order
            num_items = random.randint(1, 5)
            total_price = Decimal('0.00')

            # Make sure we don't try to sample more items than available
            num_items = min(num_items, len(products))
            selected_products = random.sample(products, num_items)

            for product in selected_products:
                quantity = random.randint(1, 3)
                price = product.price * quantity
                total_price += price

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price
                )

            # Update order total price
            order.total_price = total_price
            order.save()

            self.stdout.write(f'Created order: {order.id} with {num_items} items')

        self.stdout.write(self.style.SUCCESS('Successfully populated database'))

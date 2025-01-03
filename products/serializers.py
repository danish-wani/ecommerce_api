from rest_framework import serializers
from .models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'items', 'total_price', 'status']
        read_only_fields = ['total_price', 'status']

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("Order must contain at least one item.")

        # Validate stock availability
        for item in items:
            product = item['product']
            quantity = item['quantity']
            if product.stock < quantity:
                raise serializers.ValidationError(
                    f"Insufficient stock for product: {product.name}"
                )
        return items

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        total_price = sum(
            item['product'].price * item['quantity']
            for item in items_data
        )

        # Create order
        order = Order.objects.create(total_price=total_price, **validated_data)

        # Create order items and update stock
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

            # Update stock
            product.stock -= quantity
            product.save()

        return order

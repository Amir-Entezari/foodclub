from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .models import Food, FoodImage, Category, Customer, Cart, CartItem, Order, OrderItem, Review
from .signals import order_created


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'foods_count']
    foods_count = serializers.IntegerField(read_only=True)


class FoodImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        food_id = self.context['food_id']
        return FoodImage.objects.create(food_id=food_id, **validated_data)

    class Meta:
        model = FoodImage
        fields = ['id', 'image']


class FoodSerializer(serializers.ModelSerializer):
    images = FoodImageSerializer(many=True, read_only=True)

    class Meta:
        model = Food
        fields = ['id', 'title', 'description', 'slug',
                  'inventory', 'price', 'price_with_tax', 'category', 'images']

    category = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(), view_name='category-detail')

    price = serializers.DecimalField(
        max_digits=8, decimal_places=3, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, food: Food):
        return food.unit_price * Decimal(1.1)


class SimpleFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'title', 'unit_price']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        food_id = self.context['food_id']
        return Review.objects.create(food_id=food_id, **validated_data)
        fields = ['quantity']


class CartItemSerializer(serializers.ModelSerializer):
    food = SimpleFoodSerializer()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'food', 'quantity', 'total_price']

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.food.unit_price


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    cartitem_set = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'cartitem_set', 'total_price']

    def get_total_price(self, cart: Cart):
        return sum([cartitem.quantity * cartitem.food.unit_price for cartitem in cart.cartitem_set.all()])


class AddCartItemSerializer(serializers.ModelSerializer):
    food_id = serializers.IntegerField()

    def validate_food_id(self, value):
        if not Food.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No food with the given id')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        food_id = self.validated_data['food_id']
        quantity = self.validated_data['quantity']
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, food_id=food_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

    class Meta:
        model = CartItem
        fields = ['id', 'food_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership', ]


class OrderItemSerializer(serializers.ModelSerializer):
    food = SimpleFoodSerializer()
    #serializer_related_field=['food']
    class Meta:
        model = OrderItem
        fields = ['id', 'food', 'quantity', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at',
                  'payment_status', 'orderitem_set']
        


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError(
                'No cart with the given id found')
        if Cart.objects.filter(pk=cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty')
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            # print(self.validated_data['cart_id'])
            # print(self.context['user_id'])
            customer = Customer.objects.get(
                user_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)

            cart_items = CartItem.objects\
                .select_related('food')\
                .filter(cart_id=cart_id)

            order_items = [
                OrderItem(
                    order=order,
                    food=item.food,
                    unit_price=item.food.unit_price,
                    quantity=item.quantity
                ) for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)

            Cart.objects.filter(pk=cart_id).delete()
            order_created.send_robust(
                self.__class__,
                order=(cart_items),
                name=f'{customer.user.first_name} {customer.user.last_name}',
                email=customer.user.email)
            return order


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']

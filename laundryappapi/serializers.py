from rest_framework import serializers
from .models import Order, OrderItem, User, LaundryStore

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

class LaundryStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaundryStore
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    laundry_store = serializers.UUIDField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'laundry_store']

    def create(self, validated_data):
        laundry_store_id = validated_data.pop('laundry_store')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            laundry_store_id=laundry_store_id  # Pastikan menggunakan _id
        )
        return user

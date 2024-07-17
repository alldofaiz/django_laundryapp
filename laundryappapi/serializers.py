from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
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
        fields = ['id', 'username', 'email', 'role', 'password']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role', 'laundry_store')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            laundry_store=validated_data['laundry_store']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            # Ubah authenticate menjadi ini
            user = User.objects.get(username=username)
            if user:
                if check_password(password, user.password):
                    data['user'] = user
                else:
                    raise serializers.ValidationError("Invalid login credentials")
            else:
                raise serializers.ValidationError("User does not exist")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'")

        return data
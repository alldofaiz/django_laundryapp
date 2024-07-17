from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.crypto import get_random_string
from .models import LaundryStore, Order, User
from .serializers import OrderSerializer, UserSerializer, UserRegistrationSerializer, UserLoginSerializer, LaundryStoreSerializer

# Order ViewSet
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# LAUNDRY_STORE Views
@api_view(['GET'])
def get_all_laundry_stores(request):
    """
    Get all Laundry Stores
    """
    try:
        laundry_stores = LaundryStore.objects.all()
    except LaundryStore.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = LaundryStoreSerializer(laundry_stores, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_laundry_store(request, pk):
    """
    Get a specific Laundry Store by ID
    """
    try:
        laundry_store = LaundryStore.objects.get(pk=pk)
    except LaundryStore.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = LaundryStoreSerializer(laundry_store)
    return Response(serializer.data)

@api_view(['POST'])
def create_laundry_store(request):
    """
    Create a new Laundry Store
    """
    serializer = LaundryStoreSerializer(data=request.data)
    if serializer.is_valid():
        laundry = serializer.save()
        return Response({
            'message': 'Laundry Store was successfully created',
            'laundry_id': laundry.id  # Tambahkan koma setelah pesan
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_laundry_store(request, pk):
    """
    Delete a Laundry Store by ID
    """
    try:
        laundry_store = LaundryStore.objects.get(pk=pk)
    except LaundryStore.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    laundry_store.delete()
    return Response({'message': 'Laundry Store deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def update_laundry_store(request, pk):
    """
    Update a Laundry Store by ID
    """
    try:
        laundry_store = LaundryStore.objects.get(pk=pk)
    except LaundryStore.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = LaundryStoreSerializer(laundry_store, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Laundry Store updated successfully',
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# LOGIN USER Views
@api_view(['POST'])
def login_user(request):
    """
    Login a user and return JWT token
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'token': str(refresh.access_token),
            'refresh': str(refresh),
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# FORGET PASSWORD Views
@api_view(['POST'])
def request_password_reset(request):
    email = request.data.get('email')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    # Generate a unique token for password reset
    token = get_random_string(length=32)

    # Save the token to the user's profile (assuming you have a UserProfile model)
    user.profile.reset_password_token = token
    user.profile.save()

    # Send email with reset link
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    subject = 'Reset Your Password'
    message = f'Hi {user.username},\n\nPlease click the link below to reset your password:\n{reset_link}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

    return Response({'message': 'Password reset link sent successfully.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def confirm_password_reset(request):
    token = request.data.get('token')
    new_password = request.data.get('new_password')

    try:
        user = User.objects.get(profile__reset_password_token=token)
    except User.DoesNotExist:
        return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

    # Set new password and clear the reset token
    user.set_password(new_password)
    user.profile.reset_password_token = None
    user.save()

    return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# USER Views
@api_view(['GET'])
def get_all_users(request):
    """
    Get all Users
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_user(request, pk):
    """
    Get a specific User by ID
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
def register_user(request):
    """
    Register a new User
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        user.token = access_token  # Simpan token ke dalam database
        user.save()

        return Response({
            'message': 'User registered successfully!',
            'user_id': user.id,
            'token': access_token,
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_user(request, pk):
    """
    Delete a User by ID
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response({'message': 'User deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def update_user(request, pk):
    """
    Update a User by ID
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'User updated successfully',
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# ORDER Views
@api_view(['POST'])
def add_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message' : 'Order created successfully',
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_order_status(request, pk):
    """
    Update the status of an Order by ID
    """
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = {'status': request.data.get('status')}
    serializer = OrderSerializer(order, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Order updated successfully',
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_order(request, pk):
    """
    Delete an Order by ID
    """
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    order.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

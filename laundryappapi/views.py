from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from .models import LaundryStore, Order, OrderItem, User
from .serializers import OrderSerializer, OrderItemSerializer, UserSerializer, UserRegistrationSerializer, LaundryStoreSerializer

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
        return Response({
            'message': 'User registered successfully!',
            'user_id': user.id,
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
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# ORDER Views

@api_view(['POST'])
def add_order(request):
    """
    Add a new Order
    """
    data = request.data
    items_data = data.pop('items', [])  # Remove items from main data to process separately
    order_serializer = OrderSerializer(data=data)
    if order_serializer.is_valid():
        with transaction.atomic():
            order = order_serializer.save()

            for item_data in items_data:
                OrderItem.objects.create(
                    order=order,
                    jenis_laundry=item_data.get('jenis_laundry'),
                    jumlah_berat=item_data.get('jumlah_berat'),
                    price=item_data.get('price')
                )

        return Response({'message': 'Order created successfully!'}, status=status.HTTP_201_CREATED)
    else:
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        return Response(serializer.data)
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

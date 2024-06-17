# laundryappapi/views.py

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Order, OrderItem
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

@api_view(['POST'])
def add_order(request):
    data = request.data
    items = data.get('items', [])

    with transaction.atomic():
        order_data = {
            'hp': data.get('hp'),
            'nama': data.get('nama'),
            'tanggal_masuk': data.get('tanggal_masuk'),
            'tanggal_selesai': data.get('tanggal_selesai'),
            'catatan_khusus': data.get('catatan_khusus'),
            'total_harga': data.get('total_harga'),
            'status': '0',
        }
        order_serializer = OrderSerializer(data=order_data)
        if order_serializer.is_valid():
            order = order_serializer.save()
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    jenis_laundry=item.get('jenisLaundry'),
                    jumlah_berat=item.get('jumlahBerat')
                )
            return Response({'message': 'Order created successfully!'}, status=status.HTTP_201_CREATED)
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_order_status(request, pk):
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
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    order.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

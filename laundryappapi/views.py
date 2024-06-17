from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Laundry
from .serializers import LaundrySerializer

# ViewSet for RESTful CRUD operations
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Laundry.objects.all()
    serializer_class = LaundrySerializer

# Function-based view for adding orders
@api_view(['POST'])
def add_order(request):
    data = request.data
    items = data.get('items', [])

    with transaction.atomic():
        for item in items:
            jenis_laundry = item.get('jenis_laundry', None)  # Correct key: 'jenis_laundry'
            jumlah_berat = item.get('jumlah_berat', None)    # Correct key: 'jumlah_berat'

            if jenis_laundry is None or jumlah_berat is None:
                return Response({'error': 'Required fields are missing in items'}, status=status.HTTP_400_BAD_REQUEST)

            laundry_data = {
                'hp': data.get('hp'),
                'nama': data.get('nama'),
                'tanggal_masuk': data.get('tanggal_masuk'),
                'tanggal_selesai': data.get('tanggal_selesai'),
                'catatan_khusus': data.get('catatan_khusus'),
                'jenis_laundry': jenis_laundry,
                'jumlah_berat': jumlah_berat,
                'total_harga': data.get('total_harga'),
                'status': '0',
            }
            serializer = LaundrySerializer(data=laundry_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Laundry items created successfully!'}, status=status.HTTP_201_CREATED)




# Function-based view for updating status
@api_view(['PUT'])
def update_order_status(request, pk):
    try:
        laundry = Laundry.objects.get(pk=pk)
    except Laundry.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = {'status': request.data.get('status')}
    serializer = LaundrySerializer(laundry, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Function-based view for deleting an order
@api_view(['DELETE'])
def delete_order(request, pk):
    try:
        laundry = Laundry.objects.get(pk=pk)
    except Laundry.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    laundry.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)